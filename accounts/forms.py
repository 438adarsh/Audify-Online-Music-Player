# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    same_as_email = forms.BooleanField(required=False, label="Use email as username")

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_password", "same_as_email")

    def clean(self):
        data = super().clean()
        pwd = data.get("password")
        cpwd = data.get("confirm_password")
        if pwd and cpwd and pwd != cpwd:
            raise forms.ValidationError("Passwords do not match.")
        if data.get("same_as_email"):
            data["username"] = data.get("email")
        # Basic uniqueness checks (without customizing User model)
        if User.objects.filter(username=data.get("username")).exists():
            raise forms.ValidationError("Username already taken.")
        if User.objects.filter(email=data.get("email")).exists():
            raise forms.ValidationError("Email already registered.")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        # Allow login with email by mapping to username if needed
        username = self.data.get("username")
        from django.contrib.auth.models import User
        if username and "@" in username:
            try:
                user = User.objects.get(email=username)
                self.data = self.data.copy()
                self.data["username"] = user.username
            except User.DoesNotExist:
                pass
        return super().clean()
