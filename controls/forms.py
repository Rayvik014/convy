from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(label="answer", max_length=50)