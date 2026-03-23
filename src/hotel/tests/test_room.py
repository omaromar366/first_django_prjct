import pytest
from rest_framework.test import APIClient

from hotel.models import Room


@pytest.mark.django_db
def test_create_room() -> None:
    client = APIClient()

    data = {"description": "test", "price": 100}

    response = client.post("/rooms/", data)

    assert response.status_code == 201
    assert "room_id" in response.data
    assert Room.objects.count() == 1


@pytest.mark.django_db
def test_list_rooms() -> None:
    client = APIClient()
    Room.objects.create(description="test", price=100)
    response = client.get("/rooms/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_destroy_room() -> None:
    client = APIClient()
    room = Room.objects.create(description="test", price=100)
    response = client.delete(f"/deleteroom/{room.id}/")
    assert response.status_code == 204
    assert not Room.objects.filter(id=room.id).exists()
