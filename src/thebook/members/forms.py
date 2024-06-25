from django import forms
from django.utils.translation import gettext as _

from thebook.members.models import FeeIntervals


class NewMemberForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=100)
    email = forms.EmailField(max_length=200)
    has_key = forms.BooleanField(required=False, label=_("Has physical key?"))
    phone_number = forms.CharField(max_length=16, required=False)

    start = forms.DateField(label=_("Start Membership"))
    amount = forms.DecimalField(label=_("Membership Fee"))
    interval = forms.ChoiceField(
        choices=FeeIntervals.choices, label=_("Payment Interval")
    )
