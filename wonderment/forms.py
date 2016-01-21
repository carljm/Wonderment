from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.template.loader import render_to_string
import floppyforms.__future__ as forms

from . import models


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = models.ClassDay
        fields = ['date']

    def __init__(self, data=None, *a, **kw):
        self.session = kw.pop('session')
        super(AttendanceForm, self).__init__(data, *a, **kw)
        self.fields['date'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
        self.creating = (self.instance.pk is not None)
        self.parents = models.Parent.objects.filter(
            participations__session=self.session,
            participations__paid__gt=0,
        )
        self.children = models.Child.objects.filter(
            parent__in=self.parents)
        self.parent_formset = ParentAttendanceFormset(
            data=data.copy() if (data is not None) else None,
            instance=self.instance,
        )
        self.parent_forms_by_id = {}
        for parent_form in self.parent_formset:
            parent_form.child_forms = []
            parent_id = parent_form.instance.parent_id
            self.parent_forms_by_id[parent_id] = parent_form
        self.child_formset = ChildAttendanceFormset(
            data=data.copy() if (data is not None) else None,
            instance=self.instance,
        )
        for child_form in self.child_formset:
            parent_id = child_form.instance.child.parent_id
            parent_form = self.parent_forms_by_id[parent_id]
            parent_form.child_forms.append(child_form)

    def is_valid(self):
        return (
            self.parent_formset.is_valid() and
            self.child_formset.is_valid() and
            super(AttendanceForm, self).is_valid()
        )

    def save(self):
        classday = super(AttendanceForm, self).save(commit=False)
        classday.session = self.session
        classday.save()

        self.parent_formset.save()
        existing_parent_ids = set(models.ParentAttendance.objects.filter(
            classday=classday).values_list('parent_id', flat=True))
        new_pa = []
        for parent in self.parents:
            if parent.id not in existing_parent_ids:
                new_pa.append(
                    models.ParentAttendance(classday=classday, parent=parent))
        models.ParentAttendance.objects.bulk_create(new_pa)

        self.child_formset.save()
        existing_child_ids = set(models.ChildAttendance.objects.filter(
            classday=classday).values_list('child_id', flat=True))
        new_ca = []
        for child in self.children:
            if child.id not in existing_child_ids:
                new_ca.append(
                    models.ChildAttendance(classday=classday, child=child))
        models.ChildAttendance.objects.bulk_create(new_ca)

        return classday


class AttendanceRadioSelect(forms.RadioSelect):
    template_name = '_attendance_select.html'


ParentAttendanceFormset = inlineformset_factory(
    models.ClassDay,
    models.ParentAttendance,
    fields=['attendance'],
    extra=0,
    can_delete=False,
    widgets={'attendance': AttendanceRadioSelect},
)


ChildAttendanceFormset = inlineformset_factory(
    models.ClassDay,
    models.ChildAttendance,
    fields=['attendance'],
    extra=0,
    can_delete=False,
    widgets={'attendance': AttendanceRadioSelect},
)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ['payment']
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
            'drop_off',
            'pick_up_names',
            'on_site',
            'participate_by',
            'could_teach',
            'could_assist',
        ]
        widgets = {
            'participate_by': forms.CheckboxSelectMultiple,
        }

    def save(self):
        parent = super(ParentForm, self).save()
        if 'teaching' in parent.participate_by:
            models.Teacher.objects.update_or_create(
                parent=parent,
                defaults={
                    'name': parent.name,
                    'phone': parent.phone,
                    'phone_type': parent.phone_type,
                    'email': parent.email,
                    'address': parent.address,
                    'preferred': parent.preferred,
                },
            )
        return parent


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


class ClassSelectField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s (age %s-%s), %s: %s" % (
            obj.name,
            obj.min_age,
            obj.max_age,
            obj.teacher.name,
            obj.description,
        )


class SelectClassesForm(forms.ModelForm):
    """Form for a parent to select classes for a kid."""
    classes = ClassSelectField(
        queryset=models.Class.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = models.Child
        fields = ['parent']

    def __init__(self, *a, **kw):
        self.session = kw.pop('session')
        super(SelectClassesForm, self).__init__(*a, **kw)
        age = self.instance.age_years(as_of=self.session.start_date)
        in_classes = models.Class.objects.filter(
            students__child=self.instance, session=self.session)
        filters = Q(session=self.session)
        if age is not None:
            age_match = Q(min_age__lte=age, max_age__gte=age)
            already_in = Q(pk__in=in_classes)
            filters = filters & (age_match | already_in)
        valid_classes = models.Class.objects.filter(filters).select_related(
            'teacher')
        self.fields['classes'].queryset = valid_classes
        self.fields['classes'].initial = [c.pk for c in in_classes]

    def save(self, commit=True):
        models.Student.objects.filter(
            child=self.instance, klass__session=self.session).delete()
        for klass in self.cleaned_data['classes']:
            models.Student.objects.get_or_create(
                child=self.instance, klass=klass)
        return self.instance


class SelectClassesBaseFormSet(BaseInlineFormSet):
    """Inline formset that adds one extra form if no initial forms."""
    def __init__(self, *a, **kw):
        self.session = kw.pop('session')
        super(SelectClassesBaseFormSet, self).__init__(*a, **kw)

    def _construct_form(self, *args, **kwargs):
        kwargs.setdefault('session', self.session)
        return super(SelectClassesBaseFormSet, self)._construct_form(
            *args, **kwargs)


SelectClassesFormSet = inlineformset_factory(
    models.Parent,
    models.Child,
    form=SelectClassesForm,
    formset=SelectClassesBaseFormSet,
    extra=0,
    can_delete=False,
)
