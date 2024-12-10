# Generated by Django 5.1.4 on 2024-12-09 19:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_profile_image_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('first_Name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='نام کاربر حداقل 3 حرف و فاقد عدد باید باشد', regex="^[\\w'\\-,.][^0-9_!¡?÷?¿/\\\\+=@#$%ˆ&*(){}|~<>;:[\\]]{2,50}$")], verbose_name='نام')),
                ('last_Name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='نام خانوادگی کاربر حداقل 3 حرف و فاقد عدد باید باشد', regex="^[\\w'\\-,.][^0-9_!¡?÷?¿/\\\\+=@#$%ˆ&*(){}|~<>;:[\\]]{2,50}$")], verbose_name='نام خانوادگی')),
                ('father_Name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='نام پدر، کاربر حداقل 3 حرف و فاقد عدد باید باشد', regex="^[\\w'\\-,.][^0-9_!¡?÷?¿/\\\\+=@#$%ˆ&*(){}|~<>;:[\\]]{2,50}$")], verbose_name='نام پدر')),
                ('birth_Date', models.DateField(verbose_name='تاریخ تولد')),
                ('gender', models.BooleanField(choices=[(True, 'مرد'), (False, 'زن')], default=True, verbose_name='جنسیت')),
                ('marital_status', models.BooleanField(choices=[(True, 'مجرد'), (False, 'متاهل')], default=True, verbose_name='وضعیت تاهل')),
                ('blood_Type', models.CharField(choices=[('AB', 'AB'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('A', 'A'), ('A+', 'A+'), ('A-', 'A-'), ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'), ('O', 'O'), ('O+', 'O+'), ('O-', 'O-')], default='B+', max_length=3, verbose_name='گروه خونی')),
                ('nationality', models.BooleanField(choices=[(True, 'ایرانی'), (False, 'اتباع')], default=True, verbose_name='ملیت')),
                ('national_ID', models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='کد ملی باید ۱۰ رقم باشد', regex='^\\d{10}$')], verbose_name='کد ملی')),
                ('profile_Image', models.ImageField(default='account/profiles/default_User.png', upload_to='account/profiles', verbose_name='عکس پروفایل')),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.RegexValidator(message='ایمیل باید معتبر باشد', regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')], verbose_name='آدرس الکترونیک')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
            ],
            options={
                'verbose_name': 'شخص',
                'verbose_name_plural': 'اشخاص',
                'db_table': 'Person',
            },
        ),
        migrations.AlterField(
            model_name='address',
            name='user_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.person', verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.person', verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='tel',
            name='user_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.person', verbose_name='کاربر'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]