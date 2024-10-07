# Generated by Django 4.2.2 on 2023-08-20 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_device_corporate_donor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ram_size',
            name='size',
            field=models.PositiveIntegerField(db_column='ram_size', default=4, unique=True, verbose_name="RAM's Size(GB)"),
        ),
    ]
