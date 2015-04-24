import floppyforms.__future__ as forms

from . import models, widgets


class ResponseForm(forms.ModelForm):
    class Meta:
        model = models.Response
        fields = [
            'hear_about',
            'hear_about_other',
            'intention',
            'intention_other',
            'future_participation',
            'fall_mondays',
            'for_my_kids',
            'overall_organization',
            'overall_worthwhile',
            'help_out',
            'pay_more',
            'time_commitment',
            'timing_comments',
            'class_subjects_art',
            'class_subjects_spanish',
            'class_subjects_dance',
            'class_subjects_freeplay',
            'future_classes',
            'teachers_barbara',
            'teachers_shawnda',
            'teachers_sharon',
            'teachers_lisa',
            'teacher_comments',
            'most_valuable',
            'suggestions',
            'other_dreams',
        ]
        widgets = {
            'hear_about': forms.CheckboxSelectMultiple,
            'intention': forms.CheckboxSelectMultiple,
            'pay_more': widgets.RadioSelect,
            'time_commitment': widgets.RadioSelect,
        }
