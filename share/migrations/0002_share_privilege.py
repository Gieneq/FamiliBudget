# Generated by Django 4.1 on 2022-09-18 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='privilege',
            field=models.CharField(choices=[('View', 'View'), ('Edit', 'Edit')], default='View', max_length=8),
        ),
    ]