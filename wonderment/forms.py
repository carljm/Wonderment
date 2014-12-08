from django.forms.models import inlineformset_factory
import floppyforms.__future__ as forms

from . import models


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ['level', 'payment']
        widgets = {'payment': forms.RadioSelect}

    def __init__(self, *a, **kw):
        super(ParticipantForm, self).__init__(*a, **kw)
        formfield = self.fields['payment']
        modelfield = models.Participant._meta.get_field_by_name('payment')[0]
        formfield.choices = modelfield.get_choices(include_blank=False)


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
            'birthdate': forms.DateInput(attrs={'placeholder': 'mm/dd/yyyy'}),
        }


ChildFormSet = inlineformset_factory(
    models.Parent, models.Child, form=ChildForm, extra=5)
