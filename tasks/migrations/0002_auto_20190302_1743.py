# Generated by Django 2.1.4 on 2019-03-02 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='DueDate',
            field=models.DateField(help_text='This is the grey text'),
        ),
    ]
