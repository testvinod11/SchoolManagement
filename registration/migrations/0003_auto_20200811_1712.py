# Generated by Django 3.0.8 on 2020-08-11 17:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_teacherstudentmap_is_associate'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherstudentmap',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacherstudentmap',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
