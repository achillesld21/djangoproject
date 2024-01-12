from rest_framework import serializers
from blog.models import blog_post
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'blog_post' model.
    """
    class Meta:
        model = blog_post
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login data.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'User' model, including additional fields for user registration.
    """
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        """
        Create a new user with the given validated data.

        Parameters:
        validated_data (dict): A dictionary of the data to use to create the user.
            This dictionary should contain the following keys:
                username (str): The username for the new user.
                password (str): The password for the new user.
                first_name (str): The first name for the new user.
                last_name (str): The last name for the new user.
                email (str): The email for the new user.

        Returns:
        User: The created user.
        """
        # Extract additional fields
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        email = validated_data.pop('email', '')

        # Create user without additional fields first
        user = User.objects.create_user(**validated_data)

        # Set additional fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        # Save the user with additional fields
        user.save()

        return user
