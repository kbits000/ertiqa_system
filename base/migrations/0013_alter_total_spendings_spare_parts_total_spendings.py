# Generated by Django 4.2.2 on 2023-08-21 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_total_spendings_peripherals_total_spendings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='total_spendings',
            name='spare_parts_total_spendings',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=6),
        ),
    ]
