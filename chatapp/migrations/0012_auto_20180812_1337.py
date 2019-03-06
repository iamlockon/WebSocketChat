# Generated by Django 2.0.6 on 2018-08-12 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0011_auto_20180811_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]