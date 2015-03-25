from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory


from contacts.models import (
    Contact,
    Address,
)


class ContactForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label="Confirm email",
        required=True
    )

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'pic']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            email = kwargs['instance'].email
            kwargs.setdefault('initial', {})['confirm_email'] = email
        super(ContactForm, self).__init__(*args, **kwargs)

    def clean(self):
        if (self.cleaned_data.get('email') !=
                self.cleaned_data.get('confirm_email')):
            raise ValidationError(
                "Email address must match."
            )
        return self.cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'address', 'city', 'state', 'postal_code']

ContactAddressFormSet = inlineformset_factory(
    Contact,
    Address,
)