from rest_framework import serializers
from blog.models import blog_post

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_post
        fields = '__all__'