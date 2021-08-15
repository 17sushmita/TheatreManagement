from django.db import models
from users.models import User
# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters', blank=True)
    director = models.CharField(max_length=100)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Slot(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
       unique_together = ("date", "starttime")

    def __str__(self):
        return self.movie.name + " " + self.date.strftime("%Y-%m-%d") + " " + self.starttime.strftime("%H:%M") + " - " + self.endtime.strftime("%H:%M")

class Ticket(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user + " " + self.slot.movie.name + " " + self.slot.date.strftime("%Y-%m-%d") + " " + self.slot.starttime.strftime("%H:%M") + " - " + self.slot.endtime.strftime("%H:%M")

