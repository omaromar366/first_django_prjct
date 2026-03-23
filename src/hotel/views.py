from typing import Any

from django.db.models import QuerySet
from loguru import logger
from rest_framework import filters, generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from hotel.models import Booking, Room
from hotel.serializers import BookingSerializerCreate, BookingSerializerList, RoomSerializer


class RoomAPIList(generics.ListCreateAPIView):  # type: ignore[type-arg]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    ordering_fields = ["price", "created_at"]
    ordering = ("-created_at",)
    filter_backends = (filters.OrderingFilter,)

    @logger.catch()
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        logger.info("Запрос на создание номера: {}", request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if serializer.instance is not None:
            created_object = serializer.instance
            logger.success("Номер создан: room_id={}", created_object.id)
            return Response({"room_id": created_object.id}, status=status.HTTP_201_CREATED)
        raise APIException("Не удалось создать объект")


class RoomAPIDestroy(generics.RetrieveDestroyAPIView):  # type: ignore[type-arg]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @logger.catch()
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        room = self.get_object()
        logger.info("Удаление номера: room_id={}", room.id)
        room_id = room.id

        self.perform_destroy(room)

        logger.success("Номер удален: room_id={}", room_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingAPICreate(generics.CreateAPIView):  # type: ignore[type-arg]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializerCreate

    @logger.catch(reraise=True)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        logger.info("Запрос на создание бронирования: {}", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if serializer.instance is not None:
            created_object = serializer.instance
            logger.success("Бронирование создано: booking_id={}", created_object.id)
            return Response({"booking_id": created_object.id}, status=status.HTTP_201_CREATED)
        raise APIException("Не удалось создать объект")


class BookingAPIList(generics.ListAPIView):  # type: ignore[type-arg]
    serializer_class = BookingSerializerList

    def get_queryset(self) -> QuerySet[Booking]:
        room_idd = self.request.query_params.get("room_id")
        logger.info("Получение списка бронирований, room_id={}", room_idd)

        if not room_idd:
            logger.warning("room_id не передан")
            raise ValidationError({"room_id": "обязательное поле"})
        try:
            room_id = int(room_idd)
        except ValueError:
            logger.error("room_id должен быть числом: {}", room_idd)
            raise ValidationError({"room_id": "должен быть числом"}) from None
        queryset = Booking.objects.filter(room_id=room_id).order_by("date_start")
        logger.info("Найдено бронирований: {} для room_id={}", queryset.count(), room_id)
        return queryset


class BookingAPIDestroy(generics.RetrieveDestroyAPIView):  # type: ignore[type-arg]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializerList

    @logger.catch(reraise=True)
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        booking = self.get_object()
        logger.info("Удаление бронирования: booking_id={}", booking.id)
        booking_id = booking.id

        self.perform_destroy(booking)

        logger.success("Бронирование удалено: booking_id={}", booking_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
