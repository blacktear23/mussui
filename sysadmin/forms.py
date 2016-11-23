from django import forms


class BaseForm(forms.Form):
    pass


class ServerForm(BaseForm):
    hostname = forms.CharField(required=True)
    ip = forms.GenericIPAddressField(required=True)
    comments = forms.CharField(required=False, widget=forms.Textarea)
