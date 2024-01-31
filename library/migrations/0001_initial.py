# Generated by Django 5.0.1 on 2024-01-31 15:15

import django.db.models.deletion
import django.utils.timezone
import library.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('membership_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('is_staff', models.BooleanField(blank=True, default=False)),
                ('is_superuser', models.BooleanField(blank=True, default=False)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', library.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=200)),
                ('publishedDate', models.DateField()),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BookDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number_of_page', models.PositiveIntegerField()),
                ('publisher', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=150)),
                ('book_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
    ]
