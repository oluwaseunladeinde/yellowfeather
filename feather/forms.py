import os, re

from datetime import datetime
from django.contrib.sites.models import Site
from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.template.defaultfilters import filesizeformat
from django.utils.safestring import mark_safe
from django.utils import six
from django.forms import widgets

from account.forms import SignupForm
from account.models import EmailAddress
from account.utils import get_user_lookup_kwargs

from .models import TYPES, Profile

from pint import UnitRegistry
from model_utils import Choices

UserModel = get_user_model
ureg = UnitRegistry()

def UserModelString():
    try:
        return settings.AUTH_USER_MODEL
    except:
        return 'auth.User'

def UsernameField():
    return getattr(UserModel(), 'USERNAME_FIELD', 'username')

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now


current_year = now().year
startyear = current_year-70
endyear = current_year-18

User = UserModel()
alnum_re = re.compile(r"^\w+$")

BATHROOMS_RANGE = (
    ('', '--'),
    ('1', '1+'),
    ('2', '2+'),
    ('3', '3+'),
    ('4', '4+'),
    ('5', '5+'),
    ('6', '6+'),
    ('7', '7+'),
    ('8', '8+'),
    ('9', '9+'),
    ('10', '10+'),
)

BEDROOMS_RANGE = (
    ('', '--'),
    ('1', '1+'),
    ('2', '2+'),
    ('3', '3+'),
    ('4', '4+'),
    ('5', '5+'),
    ('6', '6+'),
    ('7', '7+'),
    ('8', '8+'),
    ('9', '9+'),
    ('10', '10+'),

############## USER ACCOUNT #########
class FeatherSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(FeatherSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'placeholder': '', 'required': 'required'})

class ProfileForm(forms.Form):
    """Override the default profile model to add a gender radio select and to
    Allow users to edit their emails on the profile page"""

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class': 'form-inline'})

    error_css_class = 'error'
    required_css_class = 'required'
    RADIO_CHOICES = [['M', 'Male'], ['F', 'Female']]

    first_name = forms.CharField(label="First Name", help_text='Your real first name would be cool',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
                                 error_messages={'required': 'Please enter real name.'})
    last_name = forms.CharField(label="Last Name", help_text='Your last name so we respect the family',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
                                error_messages={'required': 'Please enter real name.'})
    email = forms.EmailField(label="Email", help_text='A valid and active email. Just one is perfect',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
                             error_messages={'required': 'Please enter real name.'})
    about = forms.CharField(label="Bio (About you)", widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Let\'s meet you in not more than 60 words'}),
                            help_text="Tell everyone something about yourself")
    birth_date = forms.DateField(label="Date of Birth", widget=SelectDateWidget(empty_label=('Year', 'Month', 'Day'),
                                                                                years=range(startyear, endyear),
                                                                                attrs={'class': 'form-control',
                                                                                       'placeholder': 'Birthdate'}),
                                 help_text='A valid date of birth would be helpful')
    gender = forms.ChoiceField(label=_("Gender"), widget=forms.RadioSelect(attrs={'class': 'form-control'}),
                               help_text="", choices=RADIO_CHOICES)
    phone = forms.CharField(label="Mobile Number",
                            help_text='Enter a valid phone number with your country code prefix e.g. +234-1234566930',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+234-7000000000'}),
                            error_messages={'required': 'Please enter a valid phone number.'}, required=False)
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='Choose your country',
                              required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='Please choose your city',
                           required=False)
    location = forms.CharField(label='Address', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                               help_text="This is for product/service delivery purposes only.", required=False)
    url = forms.URLField(label="Website",
                         widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://'}),
                         max_length=200, help_text="http://blog.mywebsite.com", required=False)

    class Meta:
        fields = (
        'first_name', 'last_name', 'email', 'about', 'birth_date', 'gender', 'phone', 'country', 'city', 'url',
        'location')
    # exclude = ('user',)
    # widgets = {
    # 	'gender': forms.RadioSelect,
    # }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'username',
                                          'required': 'required'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'password',
                                          'required': 'required'}))


class UploadAvatarForm(forms.Form):
    avatar = forms.ImageField(label='Avatar',
                              widget=forms.ClearableFileInput(attrs={'class': 'text-center center-block'}),
                              help_text='Upload a different photo...')

    # def __init__(self, *args, **kwargs):
    # 	self.user = kwargs.pop('user')
    # 	super(UploadAvatarForm, self).__init__(*args, **kwargs)

    def clean_avatar(self):
        data = self.cleaned_data['avatar']

        if settings.AVATAR_ALLOWED_FILE_EXTS:
            root, ext = os.path.splitext(data.name.lower())
            if ext not in settings.AVATAR_ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(settings.AVATAR_ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. Authorized extensions are : %(valid_exts_list)s")
                raise forms.ValidationError(error % {'ext': ext, 'valid_exts_list': valid_exts})

        if data.size > settings.AVATAR_MAX_SIZE:
            error = _("Your file is too big (%(size)s), the maximum allowed size is (%(max_valid_size)s)")
            raise forms.ValidationError(
                error % {'size': filesizeformat(data.size), 'max_valid_size': filesizeformat(settings.AVATAR_MAX_SIZE)})

        return


class UserSettingsForm(forms.Form):
    first_name = forms.CharField(label="First Name", help_text='Your real first name would be cool',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
                                 error_messages={'required': 'Please enter real name.'})
    last_name = forms.CharField(label="Last Name", help_text='Your last name so we respect the family',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
                                error_messages={'required': 'Please enter real name.'})
    email = forms.EmailField(label="Email", help_text='A valid and active email. Just one is perfect',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
                             error_messages={'required': 'Please enter real name.'})

    # def __init__(self, *args, **kwargs):
    # 	super(UserSettingsForm, self).__init__(*args, **kwargs)
    # 	try:
    # 		self.fields['email'].initial = self.instance.user.email
    # 	except User.DoesNotExist:
    # 		pass
    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))


class ChangePasswordForm(forms.Form):
    password_current = forms.CharField(label=_("Current Password"), widget=forms.PasswordInput(render_value=False,
                                                                                               attrs={
                                                                                                   'class': 'form-control',
                                                                                                   'placeholder': ''}),
                                       help_text="Type in your current login password")
    password_new = forms.CharField(label=_("New Password"), widget=forms.PasswordInput(render_value=False,
                                                                                       attrs={'class': 'form-control',
                                                                                              'placeholder': ''}),
                                   help_text="Type in your new password")
    password_new_confirm = forms.CharField(label=_("New Password (again)"),
                                           widget=forms.PasswordInput(render_value=False,
                                                                      attrs={'class': 'form-control',
                                                                             'placeholder': ''}),
                                           help_text="Please type in your new password again. Just so we know you were certain")

    # def __init__(self, *args, **kwargs):
    # 	self.user = kwargs.pop("user")
    # 	super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get("password_current")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["password_current"]

    def clean_password_new_confirm(self):
        if "password_new" in self.cleaned_data and "password_new_confirm" in self.cleaned_data:
            if self.cleaned_data["password_new"] != self.cleaned_data["password_new_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_new_confirm"]
