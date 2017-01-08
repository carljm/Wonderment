import floppyforms.__future__ as forms

from . import (
    models,
    widgets,
)


class ResponseForm(forms.ModelForm):
    class Meta:
        model = models.Response
        fields = [
            'hear_about',
            'hear_about_other',
            'intention',
            'intention_other',
            'future_participation',
            'days',
            'for_my_kids',
            'overall_organization',
            'overall_worthwhile',
            'help_out',
            'time_commitment',
            'timing_comments',
            'class_subjects_art',
            'class_subjects_spanish',
            'class_subjects_dance',
            'class_subjects_improv',
            'class_subjects_film',
            'class_subjects_freeplay',
            'future_classes',
            'teachers_dominique',
            'teachers_lisa',
            'teachers_rachel',
            'teachers_trevor',
            'teachers_kema',
            'teachers_luke',
            'teacher_comments',
            'most_valuable',
            'suggestions',
            'other_dreams',
        ]
        widgets = {
            'hear_about': forms.CheckboxSelectMultiple,
            'intention': forms.CheckboxSelectMultiple,
            'days': forms.CheckboxSelectMultiple,
            'time_commitment': widgets.RadioSelect,
        }


class TeacherResponseForm(forms.ModelForm):
    class Meta:
        model = models.TeacherResponse
        fields = [
            'teacher_name',
            'communication',
            'communication_comments',
            'location',
            'location_comments',
            'again',
            'again_comments',
            'compensation',
            'compensation_comments',
            'assistant',
            'assistant_comments',
            'suggestions',
        ]
