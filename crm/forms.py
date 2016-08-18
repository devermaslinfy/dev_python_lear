from django import forms

from learlight.models import Customer, JewelryType


class AuthorizationForm(forms.ModelForm):
    authorized = forms.BooleanField()

    class Meta:
        model = Customer
        exclude = [
            'account', 'associate', 'first_name', 'last_name', 'email', 'address', 'city', 'county', 'state',
            'postal_code', 'country', 'phone_number', 'quote_requested', 'jewelry_type', 'jewelry_value',
            'created_by', 'updated_by'
        ]


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'phone_number']


class EmailPhotoForm(forms.ModelForm):
    jewelry_image_urls = forms.CharField(widget=forms.MultipleHiddenInput())

    class Meta:
        model = Customer
        exclude = [
            'account', 'associate', 'authorized', 'first_name', 'last_name', 'email', 'address', 'city', 'county',
            'state', 'postal_code', 'country', 'phone_number', 'quote_requested', 'jewelry_type', 'jewelry_value',
            'created_by', 'updated_by'
        ]


class QuoteCreateForm(forms.ModelForm):
    jewelry_type = forms.ModelChoiceField(
        queryset=JewelryType.objects.all(),
        empty_label='Choose one...',
        widget=forms.Select(attrs={'required': 'true'})
    )
    jewelry_value = forms.IntegerField()
    receipt_image_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    jewelry_image_urls = forms.CharField(widget=forms.MultipleHiddenInput(), required=False)

    class Meta:
        model = Customer
        exclude = [
            'account', 'associate', 'authorized', 'first_name', 'last_name', 'email', 'address', 'city', 'county',
            'state', 'postal_code', 'country', 'phone_number', 'quote_requested', 'created_by', 'updated_by'
        ]


class QuoteSummaryForm(forms.ModelForm):
    receipt_image_url = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Customer
        exclude = [
            'account', 'associate', 'authorized', 'first_name', 'last_name', 'email', 'address', 'city', 'county',
            'state', 'postal_code', 'country', 'phone_number', 'quote_requested', 'jewelry_type', 'jewelry_value',
            'created_by', 'updated_by'
        ]
