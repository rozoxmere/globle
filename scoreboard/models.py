from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Score(models.Model):
    number_of_tries = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.number_of_tries} {self.date}"