from django.db import models

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