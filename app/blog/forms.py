from django import forms
from .models import blog_post

class create_blog(forms.ModelForm):
    class Meta:
        model = blog_post
        fields = ['category','heading','content','user','image']
        widgets={
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'})
        }