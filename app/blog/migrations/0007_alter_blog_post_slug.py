# Generated by Django 4.2.8 on 2023-12-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blog_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_post',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
