# Generated by Django 4.2.1 on 2023-06-04 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='email',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]