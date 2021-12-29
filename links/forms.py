from django import forms
from qux.forms import QuxForm
from django.core.exceptions import ValidationError

from .models import *
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = "date"


class LinkForm(QuxForm):
    class Meta:
        model = Link
        fields = ["url", "title", "description", "tags", "is_favorite", "is_shared"]

    def clean_short_url(self):
        short = self.cleaned_data["short_url"]
        if short and Link.objects.filter(short_url=short).exists():
            raise ValidationError("Short URL must be unique")

        return short
