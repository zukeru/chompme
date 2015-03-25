#files.py
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
 
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required='True', max_length=30)), 
                                label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required='True',
                                                                max_length=30)), 
                                                                label=_("Email address"))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required='True', 
                                                                      max_length=30, render_value='False')), 
                                                                      label=_("Password"))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required='True', 
                                                                      max_length=30, render_value='False')), 
                                                                      label=_("Password (again)"))
    
    dob = forms.RegexField(regex=r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$', 
                           widget=forms.TextInput(attrs=dict(required='True', max_length=11)), 
                           label=_("Birthday YYYY-MM-DD"), 
                           error_messages={ 'invalid':_("This must be in the proper format YYYY-MM-DD")})
    
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required='True', max_length=20)), label=_("First Name"))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required='True', max_length=20)), label=_("Laast Name"))
    about= forms.CharField(widget=forms.TextInput(attrs=dict(required='True', max_length=90000)), label=_("About"))
    occupation = forms.CharField(widget=forms.TextInput(attrs=dict(required='True', max_length=40)), label=_("Occupation"))
    profile_title = forms.CharField(widget=forms.TextInput(attrs=dict(required='True', max_length=40)), label=_("Profile Title"))
    
    def clean_userdata(self):
        self.cleaned_data['dob'] = self.dob    
        self.cleaned_data['first_name'] = self.first_name 
        self.cleaned_data['last_name'] = self.last_name 
        self.cleaned_data['about'] = self.about 
        self.cleaned_data['occupation'] = self.occupation  
        self.cleaned_data['profile_title'] = self.profile_title 
        
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))    
        return self.cleaned_data
      