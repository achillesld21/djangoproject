from django import forms
from .models import blog_post


class CreateBlog(forms.ModelForm):
    """
    Form for creating a new blog post.
    """
    image = forms.ImageField(label='Blog Pic', required=False)


    class Meta:
        model = blog_post
        fields = ['category', 'heading', 'content', 'User', 'username', 'image']

        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'User': forms.HiddenInput(attrs={'class': 'form-control-file'}),
            'username': forms.HiddenInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('User', None)
        username = kwargs.pop('Username', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['User'].initial = user
            self.fields['User'].widget.attrs['readonly'] = True

        if username:
            self.fields['username'].initial = username
            self.fields['username'].widget.attrs['readonly'] = True


class BlogPostForm(forms.ModelForm):
    """
    Form for updating a blog post.
    """
    class Meta:
        model = blog_post
        fields = ['category', 'heading', 'content', 'image']

        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
