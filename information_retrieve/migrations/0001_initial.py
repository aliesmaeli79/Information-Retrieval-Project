# Generated by Django 4.0.6 on 2022-07-11 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileUploadModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_upload', models.FileField(upload_to='information_retrieve/document')),
            ],
        ),
    ]
