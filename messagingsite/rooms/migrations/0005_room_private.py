# Generated by Django 5.0 on 2023-12-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_alter_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
