# Generated by Django 3.0.7 on 2020-09-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='serial',
            field=models.IntegerField(default=1),
        ),
    ]
