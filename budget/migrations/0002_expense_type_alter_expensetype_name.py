# Generated by Django 4.1 on 2022-09-17 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='examples', to='budget.expensetype'),
        ),
        migrations.AlterField(
            model_name='expensetype',
            name='name',
            field=models.CharField(choices=[('Food', 'Food'), ('Fun', 'Fun'), ('Clothes', 'Clothes'), ('Eating out', 'Eating Out'), ('Car/Communication', 'Car Communication'), ('Rent/Mortgage', 'Rent Mortgage'), ('Water Bill', 'Water Bill'), ('Electric Bill', 'Electric Bill'), ('Internet Bill', 'Internet Bill'), ('Phone Bill', 'Phone Bill'), ('Loans', 'Loans'), ('Cosmetics', 'Cosmetics'), ('Health', 'Health')], default='Food', max_length=80, unique=True),
        ),
    ]
