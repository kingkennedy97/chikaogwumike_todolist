# Generated by Django 3.2.8 on 2021-10-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210322_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.FileField(null=True, upload_to='media/documents/'),
        ),
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(null=True, upload_to='media/images/'),
        ),
    ]
