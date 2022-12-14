# Generated by Django 4.1 on 2022-09-17 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_to', to='userprofile.userprofile')),
                ('shared_budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharing', to='budget.budget')),
            ],
        ),
    ]
