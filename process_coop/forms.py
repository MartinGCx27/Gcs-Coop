# Import Form libary
from django import forms
# Import Django Users model & Forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Import General info model
from coop_info.models import GeneralInformation, IdentifyInformation, UserAddressProcess, NumberContact, \
    AlternativeEmails, CotizacionImss, EconomicActivity, DataBnkRec, EconomicDependents, PersonalReferences, \
    DocumentationUser
# Import catalogues
from catalogues.models import LocationCatalogue, ActivityType
# import Betterforms
from betterforms.multiform import MultiModelForm


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


# Update user form
class UpdateUserForm(forms.ModelForm):
    class Meta:
        # Model name
        model = User
        # Form Fields
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'id_username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


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


# Update identify info
class UpdateIdentifyInforForm(forms.ModelForm):
    class Meta:
        # Model name
        model = IdentifyInformation
        # Form fields
        fields = [
            'affiliation_reason',
            'affiliate_type',
            'ceo'
        ]
        widgets = {
            'affiliation_reason': forms.Select(attrs={'class': 'form-control'}),
            'affiliate_type': forms.Select(attrs={'class': 'form-control'}),
            'ceo': forms.Select(attrs={'class': 'form-control'})
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


# Create Short General Info Form
class ShortGeneralInfoForm(forms.ModelForm):
    class Meta:
        # Model name
        model = GeneralInformation
        # Form fields
        fields = [
            'coop_age',
            'place_of_birth',
            'date_of_birth',
        ]
        widgets = {
            'place_of_birth': forms.Select(attrs={'class': 'form-control'})
        }


# Update general info
class UpdateGeneralInfoForm(forms.ModelForm):
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
        ]
        widgets = {
            'coop_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'place_of_birth': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'matrimonial_regime': forms.Select(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'})
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


# Update Address form
class UpdateUserAddressForm(forms.ModelForm):
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
            'ext_number'
        ]
        widgets = {
            'suburb': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'int_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ext_number': forms.TextInput(attrs={'class': 'form-control'})
        }


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


# Create contact number form
class ShortContactNumberForm(forms.ModelForm):
    class Meta:
        model = NumberContact
        fields = [
            'number',
            'number_type',
        ]
        widgets = {
            'number_type': forms.Select(attrs={'class': 'form-control'}),
        }


# Update contact number form
class UpdateContactNumberForm(forms.ModelForm):
    class Meta:
        model = NumberContact
        fields = [
            'number',
            'number_type',
            'status'
        ]
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
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


# Update alternative email
class UpdateAlternativeEmailForm(forms.ModelForm):
    class Meta:
        model = AlternativeEmails
        fields = [
            'alternative_email',
            'status'
        ]
        widgets = {
            'alternative_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
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


# Update IMSS register form
class UpdateCotIMSForm(forms.ModelForm):
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


# Update Economic Activity form
class UpdateEconomicActForm(forms.ModelForm):
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.none(),
                                           widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = EconomicActivity
        fields = [
            'activity',
            'activity_type',
            'activity_description',
            'status'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }


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


# Update Data Bnk Rec
class UpdateDataBnkRecForm(forms.ModelForm):
    class Meta:
        model = DataBnkRec
        fields = [
            'bnk_name',
            'account_type',
            'css_name',
            'css_number',
            'css_clave',
            'payment_method'
        ]
        widgets = {
            'css_name': forms.TextInput(attrs={'class': 'form-control'}),
            'css_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'css_clave': forms.NumberInput(attrs={'class': 'form-control'}),
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


# Update economic dependent form
class UpdateEconomicDependentForm(forms.ModelForm):
    class Meta:
        model = EconomicDependents
        fields = [
            'name',
            'ape_pat',
            'ape_mat',
            'relation',
            'birthdate',
            'age',
            'dependent_activity',
            'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ape_pat': forms.TextInput(attrs={'class': 'form-control'}),
            'ape_mat': forms.TextInput(attrs={'class': 'form-control'}),
            'relation': forms.Select(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'timezone': 'en_us'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'dependent_activity': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
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


# Update personal reference form
class UpdatePersonalRefForm(forms.ModelForm):
    class Meta:
        model = PersonalReferences
        fields = [
            'name_ref',
            'ape_pat_ref',
            'ape_mat_ref',
            'relation',
            'meet_time',
            'num_contact',
            'status'
        ]
        widgets = {
            'name_ref': forms.TextInput(attrs={'class': 'form-control'}),
            'ape_pat_ref': forms.TextInput(attrs={'class': 'form-control'}),
            'ape_mat_ref': forms.TextInput(attrs={'class': 'form-control'}),
            'relation': forms.Select(attrs={'class': 'form-control'}),
            'meet_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


# Documentation form
class DocumentationForm(forms.ModelForm):
    identification = forms.FileField(required=False)
    identification_reverse = forms.FileField(required=False)
    address_comp = forms.FileField(required=False)
    born_cert = forms.FileField(required=False)
    curp = forms.FileField(required=False)
    rfc = forms.FileField(required=False)
    cot_weeks = forms.FileField(required=False)

    class Meta:
        # Model name
        model = DocumentationUser
        # Form Fields
        fields = [
            'identification',
            'identification_reverse',
            'address_comp',
            'born_cert',
            'curp',
            'rfc',
            'cot_weeks',
            'user'
        ]


# Update User documentation
class UpdateDocumentationForm(forms.ModelForm):
    identification = forms.FileField(required=False)
    identification_reverse = forms.FileField(required=False)
    address_comp = forms.FileField(required=False)
    born_cert = forms.FileField(required=False)
    curp = forms.FileField(required=False)
    rfc = forms.FileField(required=False)
    cot_weeks = forms.FileField(required=False)
    contract_coop = forms.FileField(required=False)
    contract_user = forms.FileField(required=False)

    class Meta:
        # Model name
        model = DocumentationUser
        # Form Fields
        fields = [
            'identification',
            'identification_reverse',
            'address_comp',
            'born_cert',
            'curp',
            'rfc',
            'cot_weeks',
            'contract_coop',
            'contract_user',
        ]

# Short process form
class ShortProcessForm(MultiModelForm):
    form_classes = {
        'user_form': CreateUserForm,
        'contact_form': ShortContactNumberForm,
        'general_form': ShortGeneralInfoForm
    }