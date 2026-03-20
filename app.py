import shutil
import streamlit as st
from pathlib import Path

from config.settings import (
    GOOGLE_API_KEY,
    OPENAI_API_KEY,
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    TEMP_DIR,
    OUTPUT_DIR,
    LOG_DIR,
    TEMPLATES_DIR,
    CONFIG_DIR,
    MAX_IMAGES_PER_MODEL,
    MAX_IMAGES_TOTAL,
)
from core.db_reader import DBReader
from core.prompt_builder import PromptBuilder
from core.image_generator import ImageGenerator
from core.logger import GenerationLogger

st.set_page_config(page_title="썸네일 배경 생성기", layout="wide")
st.title("강의 썸네일 배경 이미지 생성기")


@st.cache_resource
def get_db_reader():
    return DBReader(SUPABASE_URL, SUPABASE_ANON_KEY)


@st.cache_resource
def get_prompt_builder():
    return PromptBuilder(TEMPLATES_DIR)


@st.cache_resource
def get_image_generator():
    return ImageGenerator(
        api_key=GOOGLE_API_KEY,
        models_config_path=CONFIG_DIR / "models.yaml",
        openai_api_key=OPENAI_API_KEY,
    )


def get_logger():
    return GenerationLogger(LOG_DIR / "generation_log.jsonl")


# --- Sidebar ---
with st.sidebar:
    st.header("설정")

    # Lecture search & select
    db_reader = get_db_reader()
    search_query = st.text_input("강의 검색", placeholder="강의 제목 입력...")

    if search_query:
        lectures = db_reader.search_lectures(search_query)
    else:
        lectures = db_reader.get_lectures()

    if not lectures:
        st.warning("강의를 찾을 수 없습니다.")
        st.stop()

    lecture_options = {f"{lec['product_id']} - {lec['title']}": lec for lec in lectures}
    selected_label = st.selectbox("강의 선택", options=list(lecture_options.keys()))
    selected_lecture = lecture_options[selected_label]

    st.divider()

    # Style select
    prompt_builder = get_prompt_builder()
    style_names = prompt_builder.get_style_names()
    selected_style = st.selectbox(
        "스타일 선택",
        options=list(style_names.keys()),
        format_func=lambda x: style_names[x],
    )

    st.divider()

    # Model select
    generator = get_image_generator()
    available_models = generator.get_available_models()
    selected_models = st.multiselect(
        "모델 선택 (복수 가능)",
        options=list(available_models.keys()),
        default=[list(available_models.keys())[0]],
        format_func=lambda x: available_models[x]["name"],
    )

    # Image count
    count_per_model = st.number_input(
        "모델당 생성 장수",
        min_value=1,
        max_value=MAX_IMAGES_PER_MODEL,
        value=2,
    )

    total = len(selected_models) * count_per_model
    if total > MAX_IMAGES_TOTAL:
        st.error(f"총 {total}장 요청 — 최대 {MAX_IMAGES_TOTAL}장까지 가능합니다.")

    st.divider()
    generate_btn = st.button("이미지 생성", type="primary", disabled=(total > MAX_IMAGES_TOTAL))

# --- Main Area ---
# Prompt preview
prompt = prompt_builder.build_prompt(selected_lecture, selected_style)
edited_prompt = st.text_area("프롬프트 미리보기 (수정 가능)", value=prompt, height=150)

# Generation
if generate_btn:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    with st.spinner(f"{total}장 이미지 생성 중..."):
        results = generator.generate(
            prompt=edited_prompt,
            model_keys=selected_models,
            count_per_model=count_per_model,
            output_dir=TEMP_DIR,
            lecture_id=str(selected_lecture["product_id"]),
        )

    st.session_state["results"] = results

# Display results
if "results" in st.session_state:
    results = st.session_state["results"]
    st.subheader("생성 결과")

    cols_per_row = 3
    cols = st.columns(cols_per_row)

    for idx, result in enumerate(results):
        col = cols[idx % cols_per_row]
        with col:
            if result.success and result.image_path:
                st.image(str(result.image_path), caption=f"{result.model_name} #{idx + 1}")
                if st.button(f"선택", key=f"select_{idx}"):
                    # Save as final
                    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                    final_path = OUTPUT_DIR / f"{selected_lecture['id']}_thumbnail.png"
                    shutil.copy2(result.image_path, final_path)

                    # Log all results
                    logger = get_logger()
                    for r in results:
                        logger.log(
                            lecture_id=str(selected_lecture["product_id"]),
                            model_key=r.model_key,
                            prompt=edited_prompt,
                            image_path=str(r.image_path) if r.image_path else "",
                            selected=(r is result),
                        )

                    st.success(f"저장 완료: {final_path}")
            else:
                st.error(f"{result.model_name}: {result.error}")
