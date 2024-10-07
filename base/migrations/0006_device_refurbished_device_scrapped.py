# Generated by Django 4.2.2 on 2023-08-20 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_refurbished_device_scrapped_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='refurbished',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.refurbished_device'),
        ),
        migrations.AddField(
            model_name='device',
            name='scrapped',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.scrapped_device'),
        ),
    ]
