from django.db import models
from django.utils.timezone import now


class City(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Street(models.Model):
    title = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='streets')

    def __str__(self):
        return f"{self.title}, {self.city}"


class Shop(models.Model):
    title = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shops')
    street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='shops')
    house = models.CharField(max_length=20)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.title} ({self.street}, {self.city})"

    def is_open(self):
        """
        Метод проверяет, открыт ли магазин в данный момент.
        """
        current_time = now().time()
        if self.close_time <= self.open_time:
            return self.open_time <= current_time or current_time < self.close_time
        return self.open_time <= current_time < self.close_time

