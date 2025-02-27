# Generated by Django 5.1.4 on 2025-01-03 09:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_customer_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar_profile/', verbose_name='تصویر پروفایل')),
                ('about_me', models.TextField(blank=True, null=True, verbose_name='درباره من')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_customer', to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
