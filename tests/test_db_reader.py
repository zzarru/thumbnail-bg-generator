import pytest
from unittest.mock import patch, MagicMock


def _make_mock_response(data):
    mock = MagicMock()
    mock.data = data
    return mock


class TestDBReader:
    @patch("core.db_reader.create_client")
    def test_get_lectures_returns_list(self, mock_create):
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.table.return_value.select.return_value.execute.return_value = (
            _make_mock_response([
                {"id": 1, "title": "Python 기초", "category": "웹 프로그래밍"},
                {"id": 2, "title": "딥러닝 입문", "category": "인공지능"},
            ])
        )

        from core.db_reader import DBReader
        reader = DBReader("http://fake-url", "fake-key")
        lectures = reader.get_lectures()

        assert len(lectures) == 2
        assert lectures[0]["title"] == "Python 기초"

    @patch("core.db_reader.create_client")
    def test_get_lecture_by_id(self, mock_create):
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = (
            _make_mock_response({
                "id": 1,
                "title": "Python 기초",
                "category": "웹 프로그래밍",
                "level": "입문",
                "keywords": ["python", "기초"],
                "concept": "프로그래밍 첫걸음",
                "tools": ["python", "vscode"],
            })
        )

        from core.db_reader import DBReader
        reader = DBReader("http://fake-url", "fake-key")
        lecture = reader.get_lecture_by_id(1)

        assert lecture["title"] == "Python 기초"
        assert lecture["category"] == "웹 프로그래밍"

    @patch("core.db_reader.create_client")
    def test_search_lectures(self, mock_create):
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.table.return_value.select.return_value.ilike.return_value.execute.return_value = (
            _make_mock_response([
                {"id": 1, "title": "Python 기초", "category": "웹 프로그래밍"},
            ])
        )

        from core.db_reader import DBReader
        reader = DBReader("http://fake-url", "fake-key")
        results = reader.search_lectures("Python")

        assert len(results) == 1
        assert results[0]["title"] == "Python 기초"
