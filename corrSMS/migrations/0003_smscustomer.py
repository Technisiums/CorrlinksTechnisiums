# Generated by Django 3.1.1 on 2020-10-11 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corrSMS', '0002_delete_smscustomer'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('tag', models.CharField(max_length=100)),
                ('phone_Number', models.CharField(blank=True, max_length=15)),
                ('corrlinks_Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corrSMS.customer')),
            ],
        ),
    ]
