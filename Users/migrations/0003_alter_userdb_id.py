# Generated by Django 4.2.1 on 2023-06-04 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_userdb_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]