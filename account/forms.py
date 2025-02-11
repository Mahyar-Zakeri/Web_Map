from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class loginForm(forms.Form):
    identifier = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'نام کاربری یا ایمیل'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'رمز عبور'})
    )

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')

        user = authenticate(username=identifier, password=password)
        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            raise ValidationError('نام کاربری یا رمز عبور نامعتبر است.')

        self.user = user

        return cleaned_data