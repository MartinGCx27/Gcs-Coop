# Import Form libary
from django import forms
# Import Django Users model & Forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Import coop info models
from coop_info.models import IdentifyInformation, GeneralInformation, UserAddressProcess, NumberContact, \
    AlternativeEmails, CotizacionImss, EconomicActivity, DataBnkRec, EconomicDependents, PersonalReferences
# Import catalogues
from catalogues.models import LocationCatalogue, ActivityType


# Create user form
class CreateUserForm(UserCreationForm, forms.ModelForm):
    class Meta:
        # Model name
        model = User
        # Form Fields
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]


# Identify information form
class IdentifyInforForm(forms.ModelForm):
    class Meta:
        # Model name
        model = IdentifyInformation
        # Form fields
        fields = [
            'user',
            'user_type',
            'affiliation_reason',
            'affiliate_type',
            'status_user',
            'status_reason',
            'offices_list',
            'ceo',
            'upstream_promoter'
        ]
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'affiliation_reason': forms.Select(attrs={'class': 'form-control'}),
            'affiliate_type': forms.Select(attrs={'class': 'form-control'}),
            'status_user': forms.Select(attrs={'class': 'form-control'}),
            'status_reason': forms.Select(attrs={'class': 'form-control'}),
            'offices_list': forms.Select(attrs={'class': 'form-control'})
        }


# Create General Info Form
class GeneralInfoForm(forms.ModelForm):
    class Meta:
        # Model name
        model = GeneralInformation
        # Form fields
        fields = [
            'coop_age',
            'place_of_birth',
            'date_of_birth',
            'nationality',
            'marital_status',
            'matrimonial_regime',
            'curp',
            'rfc',
            'sex',
            'user'
        ]
        widgets = {
            'place_of_birth': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'matrimonial_regime': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'})
        }


# Create User Address infor form
class UserAddressForm(forms.ModelForm):
    suburb = forms.ModelChoiceField(queryset=LocationCatalogue.objects.none(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        # Model name
        model = UserAddressProcess
        # Form fields
        fields = [
            'suburb',
            'street',
            'int_number',
            'ext_number',
            'user'
        ]


# Create contact number form
class ContactNumberForm(forms.ModelForm):
    class Meta:
        model = NumberContact
        fields = [
            'number',
            'number_type',
            'user'
        ]
        widgets = {
            'number_type': forms.Select(attrs={'class': 'form-control'}),
        }


# Create alternative email
class AlternativeEmailForm(forms.ModelForm):
    class Meta:
        model = AlternativeEmails
        fields = [
            'alternative_email',
            'user'
        ]
        widgets = {
            'alternative_email': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Create IMSS register form
class CotIMSForm(forms.ModelForm):
    class Meta:
        model = CotizacionImss
        fields = [
            'salario_cot',
        ]
        widgets = {
            'salario_cot': forms.Select(attrs={'class': 'form-control'})
        }


# Create Economic Activity form
class EconomicActForm(forms.ModelForm):
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.none(),
                                           widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = EconomicActivity
        fields = [
            'user',
            'activity',
            'activity_type',
            'activity_description'
        ]


# Create Data bnk rec form
class DataBnkRecForm(forms.ModelForm):
    class Meta:
        model = DataBnkRec
        fields = [
            'user',
            'bnk_name',
            'account_type',
            'css_name',
            'css_number',
            'css_clave',
            'payment_method'
        ]
        widgets = {
            'bnk_name': forms.Select(attrs={'class': 'form-control'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'})
        }


# Create economic dependent form
class EconomicDependentForm(forms.ModelForm):
    class Meta:
        model = EconomicDependents
        fields = [
            'user',
            'name',
            'ape_pat',
            'ape_mat',
            'relation',
            'birthdate',
            'age',
            'dependent_activity'
        ]
        widgets = {
            'relation': forms.Select(attrs={'class': 'form-control'}),
            'dependent_activity': forms.Select(attrs={'class': 'form-control'})
        }


# Create personal reference form
class PersonalRefForm(forms.ModelForm):
    class Meta:
        model = PersonalReferences
        fields = [
            'user',
            'name_ref',
            'ape_pat_ref',
            'ape_mat_ref',
            'relation',
            'meet_time',
            'num_contact'
        ]
        widgets = {
            'relation': forms.Select(attrs={'class': 'form-control'})
        }
