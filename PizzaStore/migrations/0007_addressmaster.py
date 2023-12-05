# Generated by Django 4.2.7 on 2023-11-28 03:38

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PizzaStore', '0006_remove_social_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phonenumber', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pincode', models.IntegerField()),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
    ]