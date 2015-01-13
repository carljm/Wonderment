from django.conf import settings
from django.core.mail import send_mail
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.template.loader import render_to_string
import floppyforms.__future__ as forms

from . import models


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = models.ClassDay
        fields = ['date', 'children', 'parents']
        widgets = {
            'parents': forms.CheckboxSelectMultiple,
            'children': forms.CheckboxSelectMultiple,
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ['level']


class ParentForm(forms.ModelForm):
    class Meta:
        model = models.Parent
        fields = [
            'name',
            'phone',
            'phone_type',
            'email',
            'address',
            'spouse',
            'spouse_contact',
            'emergency',
            'emergency_contact',
            'participate_by',
            'age_groups',
            'could_teach',
            'could_assist',
            'all_ages_help',
            'other_contributions',
            'classes_desired',
        ]
        widgets = {
            'participate_by': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *a, **kw):
        super(ParentForm, self).__init__(*a, **kw)
        self.fields['participate_by'].required = True


class ChildForm(forms.ModelForm):
    class Meta:
        model = models.Child
        fields = [
            'parent',
            'name',
            'birthdate',
            'special_needs',
            'gender',
        ]
        widgets = {
            'birthdate': forms.DateInput(
                format='%m/%d/%Y',
                attrs={'placeholder': 'mm/dd/yyyy'},
            ),
        }


class ConditionalExtraInlineFormset(BaseInlineFormSet):
    """Inline formset that adds one extra form if no initial forms."""
    def __init__(self, *a, **kw):
        super(ConditionalExtraInlineFormset, self).__init__(*a, **kw)
        self.extra = self.extra if self.initial_form_count() else 1


ChildFormSet = inlineformset_factory(
    models.Parent,
    models.Child,
    form=ChildForm,
    formset=ConditionalExtraInlineFormset,
    extra=0,
)


class ParticipantUrlRequestForm(forms.Form):
    """Form for a participant to request link to their registration info."""
    email = forms.EmailField()

    def clean_email(self):
        self._parents = models.Parent.objects.filter(
            email__iexact=self.cleaned_data['email'])
        if not self._parents:
            raise forms.ValidationError(
                "No previous registrant found with that email address.")

    def send(self):
        for parent in self._parents:
            context = {
                'parent': parent,
                'BASE_URL': settings.BASE_URL,
            }
            subject = "Wonderment registration link for %s" % parent.name
            body = render_to_string('emails/participant_url.txt', context)

            send_mail(
                subject, body, settings.DEFAULT_FROM_EMAIL, [parent.email])
