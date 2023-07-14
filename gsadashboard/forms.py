from django import forms

class SyncRFQS(forms.Form):
     tokenGSA = forms.CharField(label="Token de GSA", widget=forms.Textarea)
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        self.fields['tokenGSA'].widget.attrs['class'] = 'form-control'
        self.fields['tokenGSA'].widget.attrs['placeholder'] = 'Baerer token'
        self.fields['tokenGSA'].widget.attrs['id'] = 'tokenGSA'
        self.fields['tokenGSA'].widget.attrs['data-discount'] = '10%'