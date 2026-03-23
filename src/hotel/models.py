from django.db import models


class Room(models.Model):
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Room {self.id} - {self.price} - {self.description}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self) -> str:
        return f"Booking {self.id} - {self.room}"
