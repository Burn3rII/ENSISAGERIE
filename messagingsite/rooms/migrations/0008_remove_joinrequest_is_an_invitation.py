# Generated by Django 5.0 on 2023-12-28 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0007_joinrequest_is_an_invitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joinrequest',
            name='is_an_invitation',
        ),
    ]
