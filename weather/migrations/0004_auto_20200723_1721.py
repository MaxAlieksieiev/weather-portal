# Generated by Django 3.0.8 on 2020-07-23 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_auto_20200722_1435'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weather',
            options={'ordering': ['date'], 'verbose_name_plural': 'weather'},
        ),
    ]