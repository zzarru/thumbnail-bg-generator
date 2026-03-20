from supabase import create_client, Client

LECTURE_FIELDS = "product_id, title, category, level, keywords, concept, tools"


class DBReader:
    def __init__(self, url: str, key: str, table_name: str = "packt_products"):
        self.client: Client = create_client(url, key)
        self.table_name = table_name

    def get_lectures(self) -> list[dict]:
        response = (
            self.client.table(self.table_name)
            .select(LECTURE_FIELDS)
            .execute()
        )
        return response.data

    def get_lecture_by_id(self, lecture_id: int) -> dict:
        response = (
            self.client.table(self.table_name)
            .select(LECTURE_FIELDS)
            .eq("product_id", lecture_id)
            .single()
            .execute()
        )
        return response.data

    def search_lectures(self, query: str) -> list[dict]:
        response = (
            self.client.table(self.table_name)
            .select(LECTURE_FIELDS)
            .ilike("title", f"%{query}%")
            .execute()
        )
        return response.data
