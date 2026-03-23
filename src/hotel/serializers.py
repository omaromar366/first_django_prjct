from typing import Any

from rest_framework import serializers

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer[Room]):
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ("created_at", "id")

    def validate_price(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("Цена за номер должна быть больше 0")
        return value


class BookingSerializerList(serializers.ModelSerializer[Booking]):
    class Meta:
        model = Booking
        fields = (
            "id",
            "date_start",
            "date_end",
        )


class BookingSerializerCreate(serializers.ModelSerializer[Booking]):
    class Meta:
        model = Booking
        fields = (
            "room",
            "date_start",
            "date_end",
        )

    def validate(self, data: dict[str, Any]) -> dict[str, Any] | None:
        date1 = data.get("date_start")
        date2 = data.get("date_end")
        if date1 is not None and date2 is not None and date1 > date2:
            raise serializers.ValidationError(
                "Дата начала бронирования не должна быть позже даты окончания."
            )
        return data
