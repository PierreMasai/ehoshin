from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from . import utils, models
from django.forms.forms import NON_FIELD_ERRORS


class ProfileForm(ModelForm):
    """Form used to modify the user profile.

    All the editable user information have to be there, except the password which
    has is own form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def save(self, commit=True):
        """Saves this form.

        Args:
            commit: If True, then the changes to ``instance`` will be saved
            to the database.

        Returns:
            Return the instance.
        """
        return models.update_instance(self.instance, self.cleaned_data, commit)


class PasswordForm(ModelForm):
    """Form used to edit the user password.

    It consist of a field to verify the old (current) password as a protection.
    Plus two more fields to enter the new one. They have to be the same !
    """
    old = forms.CharField(label='Old password', required=False)
    new1 = forms.CharField(label='New password', required=False)
    new2 = forms.CharField(label='Confirm new password', required=False)

    class Meta:
        model = User
        fields = ('old', 'new1', 'new2')

    def clean(self):
        """Do the global validation.

        Raises:
            ValidationError: If the old (current) password is wrong
                or if the two others are not the identical.
        Returns:
            (dict): Return cleaned data.
        """
        old_password = self.cleaned_data.get('old', None)
        password1 = self.cleaned_data.get('new1', None)
        password2 = self.cleaned_data.get('new2', None)

        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Invalid password')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

    def save(self, commit=True):
        """Saves this form.

        Args:
            commit: If True, then the changes to ``instance`` will be saved
            to the database.

        Returns:
            Return the instance.
        """
        self.instance.set_password(self.cleaned_data.get('new1', None))
        return self.instance.save()


class UserForm(ModelForm):
    """Form used for the signup.

    All the editable fields have to be here (including password).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['password'].required = True

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')

    def save(self, commit=True):
        """Saves this form.

        Args:
            commit: If True, then the changes to ``instance`` will be saved
            to the database.

        Returns:
            Return the instance.
        """
        new_user = User.objects.create_user(**self.cleaned_data)
        new_user.save()

        new_user.set_password(self.cleaned_data['password'])
        return new_user.save()
