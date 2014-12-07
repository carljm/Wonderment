from django import forms
from django.forms.models import inlineformset_factory

from . import models


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


ChildFormSet = inlineformset_factory(
    models.Parent, models.Child, form=ChildForm, extra=5)
