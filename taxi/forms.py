from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class BaseDriverForm(UserCreationForm):
    LAST_DIGITS = 5
    FIRST_UPPER = 3
    LEN_ = 8

    class Meta:
        model = Driver
        additional_fields = ("first_name", "last_name", "license_number",)
        fields = UserCreationForm.Meta.fields + additional_fields

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_upper = license_number[:DriverLicenseUpdateForm.FIRST_UPPER]
        last_digits = license_number[-DriverLicenseUpdateForm.LAST_DIGITS:]
        common_part = "characters of the license must be"
        if len(license_number) != DriverLicenseUpdateForm.LEN_:
            raise ValidationError(f"License number must consist of "
                                  f"{DriverLicenseUpdateForm.LEN_} character")
        if not first_upper.isupper():
            raise ValidationError(f"First"
                                  f" {DriverLicenseUpdateForm.LAST_DIGITS} "
                                  f"{common_part} in uppercase")
        if not last_digits.isdigit():
            raise ValidationError(f"Last {DriverLicenseUpdateForm.LAST_DIGITS}"
                                  f" {common_part} digits")
        return license_number


class DriverCreationForm(BaseDriverForm, UserCreationForm):
    pass


class DriverLicenseUpdateForm(BaseDriverForm, UserCreationForm):
    pass


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
