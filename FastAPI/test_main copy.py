
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

from unittest import TestCase
from unittest.mock import MagicMock, call, create_autospec, patch

from sqlalchemy.orm import Session

from main import PopulationModel, PopulationBase


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_population():
    response = client.post(
        "/population/",
        json={"count": 2},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["count"] == 2
    #assert "id" in data
    #user_id = data["id"]

    # response = client.get(f"/users/{user_id}")
    # assert response.status_code == 200, response.text
    # data = response.json()
    # assert data["email"] == "deadpool@example.com"
    # assert data["id"] == user_id

# class MyTestCase(TestCase):
#     def test_create_new_item(self) -> None:
#         test_item = PopulationBase(x=4)
#         mock_session = create_autospec(Session, instance=True)

#         expected_output = PopulationModel.from_orm(test_item)
#         expected_session_calls = [
#             call.add(expected_output),
#             call.commit(),
#             call.refresh(expected_output),
#         ]

#         output = create_new_item(mock_session, obj_input=test_item)
#         self.assertEqual(expected_output, output)
#         self.assertListEqual(expected_session_calls, mock_session.mock_calls)
# class MyTestCase(TestCase):
#     @patch.object(PopulationBase, "from_orm")
#     def test_create_population(self, mock_from_orm: MagicMock) -> None:
#         test_item = MagicMock()
#         mock_session = create_autospec(Session, instance=True)

#         expected_output = mock_from_orm.return_value = object()
#         expected_session_calls = [
#             call.add(expected_output),
#             call.commit(),
#             call.refresh(expected_output),
#         ]

#         output = create_population(mock_session, obj_input=test_item)
#         self.assertEqual(expected_output, output)
#         self.assertListEqual(expected_session_calls, mock_session.mock_calls)

# if __name__ == '__main__':
#     unittest.main()


