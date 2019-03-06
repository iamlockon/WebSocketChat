from django import forms

class LogupForm(forms.Form):
	username = forms.CharField(label="Username",max_length=25, required=True)
	password = forms.CharField(label="Password",max_length=25, required=True)
	email = forms.EmailField(label="Email")
