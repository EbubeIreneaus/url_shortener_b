# Generated by Django 4.2.5 on 2023-09-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=10)),
                ('link', models.URLField()),
                ('qr_src', models.URLField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
