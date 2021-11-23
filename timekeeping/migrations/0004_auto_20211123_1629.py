# Generated by Django 3.2.9 on 2021-11-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timekeeping', '0003_worklog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worklog',
            options={'ordering': ('start', 'stop', 'time'), 'verbose_name': 'Worklog', 'verbose_name_plural': 'Worklog'},
        ),
        migrations.AlterField(
            model_name='worklog',
            name='time',
            field=models.DurationField(blank=True, help_text='Log manual time', verbose_name='Manual Time'),
        ),
    ]
