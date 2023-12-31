# Generated by Django 4.2.2 on 2023-07-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controls', '0005_progress_user_id_progress_word_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='chance',
            field=models.PositiveSmallIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='progress',
            name='user_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='progress',
            name='word_id',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
