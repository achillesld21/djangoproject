from rest_framework import serializers
from blog.models import blog_post
from django.contrib.auth.models import User


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_post
        fields = '__all__'