# Generated by Django 4.2.8 on 2023-12-19 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_blog_post_user_blog_post_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='user',
        ),
    ]