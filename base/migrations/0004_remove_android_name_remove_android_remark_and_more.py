# Generated by Django 4.2.2 on 2023-08-20 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_total_spendings_added_total_spendings_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='android',
            name='name',
        ),
        migrations.RemoveField(
            model_name='android',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='android',
            name='version',
        ),
        migrations.RemoveField(
            model_name='ios',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ios',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='ios',
            name='version',
        ),
        migrations.RemoveField(
            model_name='linux',
            name='name',
        ),
        migrations.RemoveField(
            model_name='linux',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='linux',
            name='version',
        ),
        migrations.RemoveField(
            model_name='macos',
            name='name',
        ),
        migrations.RemoveField(
            model_name='macos',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='macos',
            name='version',
        ),
    ]
