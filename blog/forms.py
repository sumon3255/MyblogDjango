from django import forms
from django.contrib.auth.models import User
from.models import Post,Comment,Profile

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Enter Your Text here', 'rows': '4', 'cols': '50'}))

    class Meta:
        model = Comment
        fields = ('content',)
class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = (

            'username',
            'first_name',
            'last_name',
            'email',

        )

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
