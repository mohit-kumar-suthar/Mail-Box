from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import smtplib

class Login(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=20)

    def __init__(self,*args,**Kwargs):
        super(Login,self).__init__(*args,**Kwargs)
        self.fields['email'].widget=forms.EmailInput(attrs={'class':'form-control',
        'placeholder': 'Gmail ID',
        'autocomplete':'off',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 
        'placeholder': 'Password',
        'autocomplete':'off',
        })

    def clean(self):
        cleaned_data=super(Login,self).clean()
        email=cleaned_data.get('email')
        password=cleaned_data.get('password') 
        try:
            smtp=smtplib.SMTP('smtp.gmail.com',587)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo
            smtp.login(email,password)
        except:
            raise forms.ValidationError(_('Invaild gmail or password/ Turn on less secure app access/ Allow new device first time'),code='invalid')
     

class send_form(forms.Form):
    From=forms.EmailField()
    To=forms.EmailField()
    CC=forms.EmailField(required=False,)
    BCC=forms.EmailField(required=False)
    subject=forms.CharField()
    attach=forms.FileField(required=False)
    message=forms.CharField()

    def __init__(self,*args,**kwargs):
        super(send_form,self).__init__(*args,**kwargs)
        self.fields['From'].widget=forms.EmailInput(attrs={'class':'form-control',
        'autocomplete':'off',
        'readonly':True
        })
        self.fields['To'].widget=forms.EmailInput(attrs={'class':'form-control',
        'placeholder': 'To',
        'autocomplete':'off',
        })
        self.fields['CC'].widget=forms.EmailInput(attrs={'class':'form-control',
        'placeholder': 'CC',
        'autocomplete':'off',
        })
        self.fields['BCC'].widget=forms.EmailInput(attrs={'class':'form-control',
        'placeholder': 'BCC',
        'autocomplete':'off',
        })
        self.fields['subject'].widget=forms.TextInput(attrs={'class':'form-control',
        'placeholder': 'Subject',
        'autocomplete':'off',
        })
        self.fields['attach'].widget=forms.FileInput(attrs={'class':'custom-file-input',
        'id':'customFileLang',
        'autocomplete':'off',
        })
        self.fields['message'].widget=forms.Textarea(attrs={'class':'form-control',
         'placeholder': 'Message',
        'autocomplete':'off',
        "rows":5, 
        "cols":20,
        })


    def clean(self):
        cleaned_data=super(send_form,self).clean()
        to=cleaned_data.get('To')
        cc=cleaned_data.get('CC')
        bcc=cleaned_data.get('BCC')
        From=cleaned_data.get('From')
        if to==cc!=bcc:
            raise forms.ValidationError('fields To and CC donot same')
        if cc==bcc!=to:
            if cc=='' and bcc=='':
                pass
            else:
                raise forms.ValidationError('fields CC and BCC donot same')
        if bcc==to!=cc:
            raise forms.ValidationError('fields To and BCC donot same')
        if bcc==to==cc:
            raise forms.ValidationError('fields To, CC and BCC donot same')
        if From==to:
            raise forms.ValidationError('Host email and To field donot same')
        if From==cc:
            raise forms.ValidationError('Host email and CC field donot same')
        if From==bcc:
            raise forms.ValidationError('Host email and BCC field donot same')
        
class fetch_mail(forms.Form):
    fetch=forms.CharField()
    fetch_num=forms.CharField()

    def __init__(self,*args,**kwargs):
        super(fetch_mail,self).__init__(*args,**kwargs)
        self.fields['fetch'].widget=forms.NumberInput(attrs={'class':'form-control',
        'autocomplete':'off',
        'placeholder':'Enter mail number (default show : 1)',
        })
        self.fields['fetch_num'].widget=forms.NumberInput(attrs={'class':'form-control',
        'autocomplete':'off',
        'readonly':True
        })

    def clean(self):
        cleaned_data=super(fetch_mail,self).clean()
        fetch=cleaned_data.get('fetch')
        fetch_num=cleaned_data.get('fetch_num')
        if int(fetch) > int(fetch_num) or int(fetch) < 1:
            raise forms.ValidationError('enter vaild range')
