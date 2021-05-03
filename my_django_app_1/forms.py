from django import forms
from .models import User


class AddUserIndo(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя',
                  'last_name': 'Фамилия'}

        widgets = {
            'first_name': forms.TextInput(attrs={'size': '30', 'maxlength': '100'}),
        }
