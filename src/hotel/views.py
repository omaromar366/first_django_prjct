from typing import Any

from django.db.models import QuerySet
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

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if serializer.instance is not None:
            created_object = serializer.instance
            return Response({"room_id": created_object.id}, status=status.HTTP_201_CREATED)
        raise APIException("Не удалось создать объект")


class RoomAPIDestroy(generics.RetrieveDestroyAPIView):  # type: ignore[type-arg]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingAPICreate(generics.CreateAPIView):  # type: ignore[type-arg]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializerCreate

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if serializer.instance is not None:
            created_object = serializer.instance
            return Response({"booking_id": created_object.id}, status=status.HTTP_201_CREATED)
        raise APIException("Не удалось создать объект")


class BookingAPIList(generics.ListAPIView):  # type: ignore[type-arg]
    serializer_class = BookingSerializerList

    def get_queryset(self) -> QuerySet[Booking]:
        room_idd = self.request.query_params.get("room_id")

        if not room_idd:
            raise ValidationError({"room_id": "обязательное поле"})
        try:
            room_id = int(room_idd)
        except ValueError:
            raise ValidationError({"room_id": "должен быть числом"}) from None

        return Booking.objects.filter(room_id=room_id).order_by("date_start")


class BookingAPIDestroy(generics.RetrieveDestroyAPIView):  # type: ignore[type-arg]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializerList


# class RoomCreateAPIView(APIView):
#     def post(self, request):
#         serializer = RoomSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def get(self, request):
#         rooms = Room.objects.all()
#         sort_by = request.query_params.get('sort_by')
#         order = request.query_params.get('order')
#         allowed_fields = ['created_at', 'price']
#         order = (order or "").lower()
#         if sort_by and sort_by in allowed_fields:
#             if order == 'desc':
#                 field = '-' + sort_by
#             else:
#                 field = sort_by
#             rooms = rooms.order_by(field)
#
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)
#
#     def delete(self, request):


# Create your views here.
