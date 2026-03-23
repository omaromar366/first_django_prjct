from django.urls import path

from . import views

urlpatterns = [
    path("/roomslist/", views.RoomAPIList.as_view()),
    # path("rooms/list", views.list_rooms),
    # path("rooms/delete", views.delete_room),
    #
    # path("booking/create", views.create_booking),
    # path("booking/list", views.list_booking),
    # path("booking/delete", views.delete_booking),
]
