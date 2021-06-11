import unicodedata
from django import forms
from django.forms import ModelForm
from .models import Simulation, Locality, UserProfile
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

UserModel = get_user_model()

####
# Defines the various forms used throughout the web app.
####

# SignUpForm extends the basic Django UserCreationForm and adds an extra field that needs to be given, an email.
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=256, help_text="Provide a valid email address.")
    
    class Meta: 
        model = User #Associates the form to a model of the project
        fields = ('username', 'email', 'password1', 'password2')

# FeedbackForm is used for the feedback/questions page, needs an email and message to submit properly.
class FeedbackForm(forms.Form):
    name = forms.CharField(required=True, label="Full Name")
    email = forms.EmailField(required=True)
    organization = forms.CharField(required=True, label="Organization/Affiliation")
    message = forms.CharField(widget=forms.Textarea, required=True)


class SimulationForm(forms.ModelForm):
    # Form for creating a project analysis
    class Meta:
        # app_attributes = {'oninvalid': 'this.setCustomValidity("Application field is required")', 'oninput': 'this.setCustomValidity("")', 'class':'form-control', 'min':0}
        model = Simulation #Defines that the fields of this form correspond to the Simulation model
        fields = ('user', 'name','initial_year', 'project_length', 'initial_investment', 'project_size', 'total_acreage', 'inside_fence_acreage', 'baseline_land_value', 'inside_fence_land_value', 'outside_fence_land_value', 'dominion_or_apco')
        labels = {
            # Labels for each field of the form
            'name': ugettext_lazy('Project Name'),
            'initial_investment': ugettext_lazy('Total Capitalized Investment ($)'),
            'initial_year': ugettext_lazy('Initial Year'),
            'project_length': ugettext_lazy('Project Length (Years)'),
            'project_size': ugettext_lazy('Project Size (MW)'),
            'total_acreage': ugettext_lazy('Total Project acreage (Acres)'),
            'inside_fence_acreage': ugettext_lazy('Solar Project Inside the Fence (Acres)'),
            'baseline_land_value': ugettext_lazy('Baseline Value of Land ($)'),
            'inside_fence_land_value': ugettext_lazy('Inside the Fence Value of Land ($)'),
            'outside_fence_land_value': ugettext_lazy('Outside the Fence Value of Land ($)'),
            'dominion_or_apco': ugettext_lazy('Is the project operated by either an electric supplier, electric company (Dominion, APCo, Old Dominion Power) or an electric cooperative?'),
        }
        widgets = {
            # Defines the input expected for each field of the form and sets minimum and maximum values for the inputs.
            'user': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'initial_year': forms.NumberInput(attrs={'class': 'form-control', 'min':2020, 'max':2050}),
            'project_length': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'initial_investment': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'project_size': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'total_acreage': forms.NumberInput(attrs={'class':'form-control', 'min':0}),
            'inside_fence_acreage': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'baseline_land_value': forms.NumberInput(attrs={'class': 'form-control', 'min':100}),
            'inside_fence_land_value': forms.NumberInput(attrs={'class': 'form-control', 'min':100}),
            'outside_fence_land_value': forms.NumberInput(attrs={'class': 'form-control', 'min':100}),
            'dominion_or_apco': forms.CheckboxInput(attrs={'style': 'width:30px;height:35px;position:relative;top: 10px; margin:0 20px;'}), #adds some styling to the checkbox, couldn't do it using css for some reason
        }

class UserProfileUpdateForm(forms.ModelForm):
    # Form for updating user parameters
    class Meta:
        model = UserProfile
        fields = ('discount_rate', 'mt_tax_rate', 'real_property_rate', 'assessment_ratio', 'baseline_true_value', 'adj_gross_income', 'taxable_retail_sales', 'population', 'adm', 'required_local_matching', 'budget_escalator', 'years_between_assessment', 'use_composite_index')
        labels = {
            #'revenue_share_rate': ugettext_lazy("Revenue Share Rate ($/MW)"), 
            'discount_rate': ugettext_lazy("Discount Rate (%)"), 
            'mt_tax_rate': ugettext_lazy("M&T Tax Rate ($/ $100 Assessed Value)"), 
            'real_property_rate': ugettext_lazy("Real Property Rate ($/ $100 Assessed Value)"), 
            'assessment_ratio': ugettext_lazy("Assessment Ratio (%)"), 
            'baseline_true_value': ugettext_lazy("Baseline True Value ($)"), 
            'adj_gross_income': ugettext_lazy("Adjusted Gross Income ($)"), 
            'taxable_retail_sales': ugettext_lazy("Taxable Retail Sales ($)"), 
            'population': ugettext_lazy("Population"), 
            'adm': ugettext_lazy("Average Daily Student Membership (ADM)"), 
            'required_local_matching': ugettext_lazy("Required Local Matching ($):"),
            'budget_escalator': ugettext_lazy("Budget Escalator (%)"), 
            'years_between_assessment': ugettext_lazy("Years Between Assessment"),
            'use_composite_index': ugettext_lazy("Use Composite Index for Calculations?"),
        }
        help_texts = {
            'required_local_matching': ugettext_lazy("Enter the sum of locality's Required Local Effort (RLE) for Standards of Quality and Required Local Match (RLM) for Incentive and Lottery Accounts."),
        } # Defines a help text to be displayed under the form entry box to help define the variable for the user.
        widgets = {
            #'revenue_share_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':1400}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'mt_tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'real_property_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'assessment_ratio': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'baseline_true_value': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'adj_gross_income': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'taxable_retail_sales': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'population': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'adm': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'required_local_matching': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'budget_escalator': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'years_between_assessment': forms.NumberInput(attrs={'class': 'form-control', 'min':1, 'max':30}),
            'use_composite_index': forms.CheckboxInput(attrs={'style': 'width:30px;height:35px;position:relative;top: 10px; margin:0 20px;'}),
        }


## Code used to send password reset email and form when a user requests.

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()

# Defines a form for password reset, requires email and username to submit. On a submit if the form is correctly filled out
# an email will be sent to the email entered. 
class PasswordResetUsernameForm(forms.Form):
    email = forms.EmailField(
        label=ugettext_lazy("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    user = forms.CharField(
        label=ugettext_lazy("Username"),
        max_length = 150,
    )

    #Function to send email to user
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email, users):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        user = UserModel.USERNAME_FIELD
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            '%s__iexact' % user: users,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        username = self.cleaned_data["user"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email, username):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )