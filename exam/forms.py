from django import forms

class AnswerImageForm( forms.Form ):
    image = forms.ImageField()
