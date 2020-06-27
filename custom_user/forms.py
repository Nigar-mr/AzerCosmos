from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from .models import MyUser

# get custom user
# User = MyUser()


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = MyUser
        fields = ("username", "email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_(
                                             "Raw şifrələr bazada saxlanmır, onları heç cürə görmək mümkün deyil "
                                             "bu istifadəçinin şifrəsidir, lakin siz onu dəyişə bilərsiziniz "
                                             " <a href=\"../password/\">bu form</a>. vasitəsilə"))

    class Meta:
        model = MyUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class RegisterForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("Sifreler bir birleriyle uygunlasmadi."),
        "is_active": _("Active user oldugunuzu qeyd edin."),
    }

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            'type': "password",
            'name': "pass",
            "placeholder": "Password"
        }
    ))
    confirm_password = forms.CharField(label="Repeat password", widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            'type': "password",
            'name': "repeat-pass",
            "placeholder": "Confrim Password"
        }
    ))

    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'username', 'email'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'name': "first_name",
                'type': "text",
                'class': "form-control",
                'placeholder': "Name"
            }),
            'last_name': forms.TextInput(attrs={
                'name': "last_name",
                'type': "text",
                'class': "form-control",
                'placeholder': "Surname"
            }),
            'username': forms.TextInput(attrs={
                'name': "username",
                'type': "text",
                'class': "form-control",
                'placeholder': "Username"
            }),
            'email': forms.TextInput(attrs={
                'name': "email",
                'type': "email",
                'class': "form-control",
                'placeholder': "Email"
            }),
        }
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return confirm_password


class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
         'username', 'password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'name': "username",
                'type': "text",
                'class': "form-control",
                'placeholder': "UserName"
            }),
            'password': forms.TextInput(attrs={
                'name': "password",
                'type': "text",
                'class': "form-control",
                'placeholder': "Password"
            })
        }


class SettingProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'avatar']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'input2',
                'type': 'text'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'input6',
                'type': 'text'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'input6',
                'type': 'text'
            })
        }
        labels = {
            'username': 'Username',
            'first_name': 'Name',
            'last_name': 'Surname',
            'avatar': 'Profile Image'

        }


class PasswordChangeForm(forms.Form):
    new_passw = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'New password'

        }
    ))
    verify_passw = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Confrim Password'
        }
    ))


    def clean(self):
        new_password = self.cleaned_data.get("new_passw")
        verify_password = self.cleaned_data.get('verify_passw')
        if new_password != verify_password:
            raise forms.ValidationError("Not equal")

    def save(self, user, commit=True):
        password = self.clean()
        user.set_password(password)
        if commit:
            user.save()
        return user
