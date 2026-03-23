import pytest
from rest_framework.test import APIClient

from hotel.models import Booking, Room


@pytest.mark.django_db
def test_create_booking() -> None:
    client = APIClient()
    room = Room.objects.create(description="test", price=100)
    data = {
        "room": room.id,
        "date_start": "2026-04-01",
        "date_end": "2026-04-03",
    }

    response = client.post("/createbook/", data)

    assert response.status_code == 201
    assert "booking_id" in response.data


@pytest.mark.django_db
def test_list_booking() -> None:
    client = APIClient()
    room = Room.objects.create(description="test", price=100)
    data = {
        "room": room.id,
        "date_start": "2026-04-01",
        "date_end": "2026-04-03",
    }
    Booking.objects.create(room=room, date_start="2026-04-01", date_end="2026-04-03")
    response = client.get(f"/booking/?room_id={data.get('room')}")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_delete_booking() -> None:
    client = APIClient()
    room = Room.objects.create(description="test", price=100)
    booking = Booking.objects.create(room=room, date_start="2026-04-01", date_end="2026-04-03")
    response = client.delete(f"/deletebook/{booking.id}/")
    assert response.status_code == 204
    assert not Booking.objects.filter(id=booking.id).exists()
