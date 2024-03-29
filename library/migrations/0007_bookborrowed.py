# Generated by Django 5.0.1 on 2024-01-31 15:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_delete_customuser_alter_user_id_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookBorrowed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('borrowed_date', models.DateField()),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
