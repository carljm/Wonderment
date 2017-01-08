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
            'contributing',
            'contributing_other',
            'days',
            'for_my_kids',
            'overall_organization',
            'overall_worthwhile',
            'help_out',
            'time_commitment',
            'timing_comments',
            'class_subjects_cooking',
            'class_subjects_chemistry_12_18',
            'class_subjects_advanced_film',
            'class_subjects_super_cool_art',
            'class_subjects_chemistry_8_11',
            'class_subjects_needs',
            'class_subjects_zoology',
            'class_subjects_art_outer_space',
            'class_subjects_music',
            'class_subjects_art',
            'class_subjects_outdoor',
            'class_subjects_sensory',
            'class_subjects_music_together',
            'teachers_dominique',
            'teachers_keisha',
            'teachers_kyle',
            'teachers_monica',
            'teachers_kema',
            'teachers_christie',
            'teachers_dyani',
            'teachers_karissa',
            'teachers_kathrin',
            'teachers_luke',
            'teacher_comments',
            'most_valuable',
            'class_ideas_3_5',
            'class_ideas_3_5_other',
            'class_ideas_5_7',
            'class_ideas_5_7_other',
            'class_ideas_8_11',
            'class_ideas_8_11_other',
            'class_ideas_teen',
            'class_ideas_teen_other',
            'suggestions',
            'other_dreams',
        ]
        widgets = {
            'hear_about': forms.CheckboxSelectMultiple,
            'intention': forms.CheckboxSelectMultiple,
            'contributing': forms.CheckboxSelectMultiple,
            'days': forms.CheckboxSelectMultiple,
            'time_commitment': widgets.RadioSelect,
            'class_ideas_3_5': forms.CheckboxSelectMultiple,
            'class_ideas_5_7': forms.CheckboxSelectMultiple,
            'class_ideas_8_11': forms.CheckboxSelectMultiple,
            'class_ideas_teen': forms.CheckboxSelectMultiple,
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
