from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    password_validation,
)
from django.forms import ModelForm

from api.models import Policy


class RegisterForm(forms.ModelForm):
    email2 = forms.EmailField(label="Re-enter Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()
        self.fields["dob"].widget = forms.SelectDateWidget()

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "email2",
            "password",
            "dob",
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("First name is required")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Last name is required")
        return last_name

    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if not dob:
            raise forms.ValidationError("Date of birth is required")
        return dob

    def clean_password(self):
        password = self.cleaned_data["password"]
        password_validation.validate_password(password, self.instance)
        return password

    def clean(self):
        data = self.cleaned_data
        if not data.get("email2") == data.get("email"):
            raise forms.ValidationError("The two emails don't match")

        email = data.get("email2")
        password = data.get("password")
        if authenticate(username=email, password=password):
            # Need to skip super to not validate unique fields
            return data
        return super().clean()


# form to create a new Policy
class PolicyForm(ModelForm):
    class Meta:
        model = Policy
        fields = ("type", "premium", "cover", "state")
