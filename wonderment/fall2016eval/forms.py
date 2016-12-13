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
            'contributing',
            'contributing_other',
            'days',
            'for_my_kids',
            'overall_organization',
            'overall_worthwhile',
            'help_out',
            'time_commitment',
            'timing_comments',
            'class_subjects_art_5_7',
            'class_subjects_art_12_18',
            'class_subjects_preschool_exploration',
            'class_subjects_music_together',
            'class_subjects_physics_8_11',
            'class_subjects_physics_12_18',
            'class_subjects_film',
            'class_subjects_bee_science',
            'teachers_dyani',
            'teachers_heather',
            'teachers_kyl',
            'teachers_keisha',
            'teachers_kiah',
            'teachers_luke',
            'teacher_comments',
            'most_valuable',
            'class_ideas',
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
