from django.db import models
from django.contrib.auth.models import User

class Sector(models.Model):
    sectors = models.CharField(max_length=20, db_index=True, verbose_name='Sector')

    class Meta:
        verbose_name_plural = 'Sectors'
        verbose_name = 'Sector'
        ordering = ['-id']

    def __str__(self):
        return self.sectors

class Word(models.Model):
    lang1 = models.CharField(max_length=50, verbose_name='English')
    lang2 = models.CharField(max_length=50, verbose_name='Russian')
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, verbose_name='Sector')

    class Meta:
        verbose_name_plural = 'Words'
        verbose_name = 'Word'
        ordering = ['lang1']

    def __str__(self):
        return self.lang1

class Progress(models.Model):
    user_id = models.PositiveIntegerField(default=0, verbose_name='User_ID')
    word_id = models.PositiveSmallIntegerField(default=0, verbose_name='Word_ID')
    chance = models.PositiveSmallIntegerField(default=50, verbose_name='Chance')

    class Meta:
        verbose_name_plural = 'Progress'
        verbose_name = 'Progress'
        ordering = ['-user_id']




