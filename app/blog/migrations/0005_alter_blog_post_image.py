# Generated by Django 4.2.8 on 2023-12-07 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blog_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_post',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
