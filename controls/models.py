from django.db import models
from django.contrib.auth.models import User

class Sector(models.Model):
    sectors = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.sectors

class Word(models.Model):
    lang1 = models.CharField(max_length=50)
    lang2 = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.lang1

class Progress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    word_id = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True)
    chance = models.ValueRange(start=0.1, end=99.9)


