from django import forms
from .models import blog_post


class CreateBlog(forms.ModelForm):
    class Meta:
        model = blog_post
        fields = ['category', 'heading', 'content', 'User', 'image']

        image = forms.ImageField(label='Blog Pic', required=False)

        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'User': forms.Select(attrs={'class': 'form-control-file'})
        }
