# Generated by Django 2.0.2 on 2018-05-14 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smite', '0003_auto_20180514_2106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemdescription',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='itemstat',
            old_name='item_id',
            new_name='item',
        ),
    ]