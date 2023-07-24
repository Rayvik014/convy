from django import forms
from django.contrib.auth.forms import PasswordResetForm


class AnswerForm(forms.Form):
    answer = forms.CharField(label="answer", max_length=50)
    offered_answer = forms.CharField(label="offered_answer")
    offered_id = forms.IntegerField(label="offered_id")

class LoginForm(forms.Form):
    email_value = forms.EmailField(label="email_value", max_length=254)
    password_value = forms.CharField(label="password_value", max_length=50)

class RegistrationForm(forms.Form):
    user_name = forms.CharField(label="user_name", max_length=50)
    user_email = forms.EmailField(label="user_email", max_length=254)
    user_password_1 = forms.CharField(min_length=6, max_length=50)
    user_password_2 = forms.CharField(min_length=6, max_length=50)

class NewPasswordForm(forms.Form):
    user_password_1 = forms.CharField(min_length=6, max_length=50)
    user_password_2 = forms.CharField(min_length=6, max_length=50)

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, max_length=254)

