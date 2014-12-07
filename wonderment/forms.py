from django import forms
from django.forms.models import inlineformset_factory

from . import models


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ['level']


class ParentForm(forms.ModelForm):
    class Meta:
        model = models.Participant
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
            'could_teach',
            'could_assist',
            'all_ages_help',
            'other_contributions',
            'classes_desired',
        ]


class ChildForm(forms.ModelForm):
    class Meta:
        model = models.Child
        fields = [
            'name',
            'birthdate',
            'special_needs',
            'gender',
        ]


ChildFormSet = inlineformset_factory(
    models.Participant, models.Child, form=ChildForm, extra=5)
