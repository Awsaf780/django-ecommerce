# Generated by Django 3.1.3 on 2020-11-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20201120_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]