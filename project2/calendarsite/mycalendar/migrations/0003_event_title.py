# Generated by Django 3.0.3 on 2020-02-14 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0002_auto_20200214_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(default='default', max_length=50),
            preserve_default=False,
        ),
    ]
