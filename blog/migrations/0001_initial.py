# Generated by Django 3.0.7 on 2020-09-01 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('authur', models.CharField(max_length=13)),
                ('timeStamp', models.DateTimeField(blank=True)),
            ],
        ),
    ]