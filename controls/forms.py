from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(label="answer", max_length=50)
    offered_answer = forms.CharField(label='offered_answer')
    offered_id = forms.IntegerField(label='offered_id')

class LoginForm(forms.Form):
    email_value = forms.EmailField(label="email_value")
    password_value = forms.CharField(label='password_value')