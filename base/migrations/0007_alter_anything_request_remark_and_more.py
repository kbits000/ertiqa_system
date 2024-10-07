# Generated by Django 4.2.2 on 2023-08-20 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_device_refurbished_device_scrapped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anything_request',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='anything_request',
            name='remark_response',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='computer_peripheral',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Remark/Description'),
        ),
        migrations.AlterField(
            model_name='computer_spare_part',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Remark/Description'),
        ),
        migrations.AlterField(
            model_name='device',
            name='corporate_donor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.corporate_donor'),
        ),
        migrations.AlterField(
            model_name='device',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='device_refurbishment_request',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='device_refurbishment_request',
            name='remark_response',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='inspect_peripheral_request',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='inspect_peripheral_request',
            name='remark_response',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='software',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Remark/Description'),
        ),
        migrations.AlterField(
            model_name='spare_part_peripheral_device_request',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='spare_part_peripheral_device_request',
            name='remark_response',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='windows',
            name='remark',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
