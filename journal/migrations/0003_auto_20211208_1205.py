# Generated by Django 3.2.9 on 2021-12-08 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20211208_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='occasion',
            field=models.DateField(blank=True, help_text='Date the entry was made', verbose_name='Occasion'),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set(),
        ),
    ]
