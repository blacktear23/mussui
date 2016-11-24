from django import forms
from db.models import *


class BaseForm(forms.Form):
    pass


class ServerForm(BaseForm):
    hostname = forms.CharField(required=True)
    ip = forms.GenericIPAddressField(required=True)
    status = forms.CharField(required=True)
    encryption = forms.CharField(required=True)
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def clean_status(self):
        status = self.cleaned_data['status']
        s = Server()
        if status not in s.STATUS:
            raise forms.ValidationError("Invalid status")
        return status

    def clean_encryption(self):
        value = self.cleaned_data['encryption']
        s = Server()
        if value not in s.ENCRYPTION_METHODS:
            raise forms.ValidationError("Invalid encryption")
        return value
