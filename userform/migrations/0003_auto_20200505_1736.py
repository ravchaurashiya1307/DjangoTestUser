# Generated by Django 3.0.5 on 2020-05-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userform', '0002_auto_20200505_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newuser',
            old_name='pn',
            new_name='Phone',
        ),
        migrations.AlterField(
            model_name='newuser',
            name='image',
            field=models.ImageField(upload_to='pics/'),
        ),
    ]
