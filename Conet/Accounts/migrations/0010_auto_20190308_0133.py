# Generated by Django 2.1.5 on 2019-03-08 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0009_auto_20190308_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.CharField(default='127.0.1.1', max_length=50),
        ),
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(default='127.0.1.1/author/<django.db.models.fields.UUIDField>/', max_length=100),
        ),
    ]
