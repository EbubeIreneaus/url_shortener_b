# Generated by Django 4.2.5 on 2023-10-02 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='qr_src',
            field=models.URLField(max_length=30),
        ),
    ]