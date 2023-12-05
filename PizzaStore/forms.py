from django import forms
from .models import AddressMaster


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressMaster
        fields=['first_name','last_name','email','phonenumber','address','city','state','pincode','country']