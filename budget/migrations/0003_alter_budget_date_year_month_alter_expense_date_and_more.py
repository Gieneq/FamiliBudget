# Generated by Django 4.1 on 2022-09-18 23:34

import datetime
from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_expense_type_alter_expensetype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='date_year_month',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='expensetype',
            name='name',
            field=models.CharField(choices=[('Food', 'Food'), ('Fun', 'Fun'), ('Clothes', 'Clothes'), ('Eating out', 'Eating Out'), ('Car Communication', 'Car Communication'), ('Rent Mortgage', 'Rent Mortgage'), ('Water Bill', 'Water Bill'), ('Electric Bill', 'Electric Bill'), ('Internet Bill', 'Internet Bill'), ('Phone Bill', 'Phone Bill'), ('Loans', 'Loans'), ('Cosmetics', 'Cosmetics'), ('Health', 'Health')], default='Food', max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='value',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=14),
        ),
    ]
