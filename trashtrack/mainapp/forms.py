from django import forms
from django.contrib.auth.models import User
from .models import CompanyProfile

class CompanySignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'address', 'contact_number', 'email']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        company_profile = super().save(commit=False)
        company_profile.user = user
        if commit:
            company_profile.save()
        return company_profile
