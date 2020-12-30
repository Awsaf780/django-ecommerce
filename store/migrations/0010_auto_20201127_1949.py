# Generated by Django 3.1.3 on 2020-11-27 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20201127_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('apparel-men', 'Apparel-men'), ('apparel-women', 'Apparel-women'), ('apparel-kids', 'Apparel-kids'), ('electronics-smartphone', 'Electronics-smartphone'), ('electronics-accessory', 'Electronics-accessory'), ('electronics-computer', 'Electronics-computer'), ('fashion-footwear', 'Fashion-footwear'), ('fashion-watch', 'Fashion-watch'), ('fashion-accessory', 'Fashion-accessory'), ('fashion-cosmetic', 'Fashion-cosmetic'), ('misc', 'Misc')], default='', max_length=200, null=True),
        ),
    ]