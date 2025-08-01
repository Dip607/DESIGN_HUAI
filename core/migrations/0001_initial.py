# Generated by Django 5.2.3 on 2025-07-28 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('labels', models.TextField(blank=True, null=True)),
                ('dominant_colors', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
