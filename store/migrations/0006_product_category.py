# Generated by Django 3.1.3 on 2020-11-18 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20201117_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Apparel-men', 'Apparel-men'), ('Apparel-women', 'Apparel-women'), ('Apparel-kids', 'Apparel-kids'), ('Electronics-smartphone', 'Electronics-smartphone'), ('Electronics-accessory', 'Electronics-accessory'), ('Electronics-computer', 'Electronics-computer'), ('Fashion-footwear', 'Fashion-footwear'), ('Fashion-watch', 'Fashion-watch'), ('Fashion-accessory', 'Fashion-accessory'), ('Fashion-cosmetic', 'Fashion-cosmetic'), ('Misc', 'Misc')], default='', max_length=200, null=True),
        ),
    ]
