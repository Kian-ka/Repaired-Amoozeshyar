# Generated by Django 5.1.4 on 2024-12-09 19:48

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_person_alter_address_user_id_alter_employee_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_Date',
            field=django_jalali.db.models.jDateField(verbose_name='تاریخ تولد'),
        ),
    ]