from .models import Post, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


#Форма регистрации
class RegistrationForm(UserCreationForm):
    avatar = forms.ImageField()
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")  # Добавляем поле bio

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'bio', 'password1')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.TextInput(attrs={'class': 'form-input'}),
        }


#Форма редактирования
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'bio' )

    avatar = forms.ImageField(label="Аватар", required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")  # Добавляем поле bio

#Форма авторизация
class LoginForm(AuthenticationForm):
    pass


#Форма удаления аккаунта
class DeleteAccountForm(forms.Form):
    confirm_delete = forms.BooleanField(label='Удалить аккаунт', required=True)


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
