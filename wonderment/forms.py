from datetime import datetime
import json

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.forms.models import (
    inlineformset_factory, BaseInlineFormSet, ModelChoiceIterator)
from django.template.loader import render_to_string
from django.utils import timezone
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
            models.Teacher.objects.get_or_create(parent=parent)
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


class SmartLabelModelChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        """Return the choice tuple for the given object."""
        return (
            self.field.prepare_value(obj),
            SmartLabel(obj, self.field),
            )


class SmartLabel:
    """
    A select-widget option label with smarts: also stores option attributes.

    Allows us to squeeze more data into the "label" half of the label-value
    pair of a multiple-select choice. Behaves like a simple text label if
    coerced to unicode, but also has "attrs" and "obj" attributes to access
    attributes for the choice/option, and the object itself. Useful for
    advanced multi-select widgets.

    """
    def __init__(self, obj, field):
        self.field = field
        self.obj = obj

    def __str__(self):
        return self.field.label_from_instance(self.obj)


class SelectClassesCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'class_select_widget.html'


class ClassSelectField(forms.ModelMultipleChoiceField):
    widget = SelectClassesCheckboxSelectMultiple

    def when(self, obj):
        start_ap = obj.start.strftime('%p').lower()
        end_ap = obj.end.strftime('%p').lower()
        if start_ap == end_ap:
            start_ap = ''
        start_mins = obj.start.strftime('%M')
        if start_mins == '00':
            start_mins = ''
        else:
            start_mins = ':' + start_mins
        end_mins = obj.end.strftime('%M')
        if end_mins == '00':
            end_mins = ''
        else:
            end_mins = ':' + end_mins
        return "%s %s%s%s-%s%s%s" % (
            obj.get_weekday_display(),
            obj.start.strftime('%-I'),
            start_mins,
            start_ap,
            obj.end.strftime('%-I'),
            end_mins,
            end_ap,
        )

    def label_from_instance(self, obj):
        return "%s: %s (age %s-%s), %s: %s" % (
            self.when(obj),
            obj.name,
            obj.min_age,
            obj.max_age,
            obj.teacher.name,
            obj.description,
        )

    def _get_choices(self):
        """Use MTModelChoiceIterator."""
        if hasattr(self, "_choices"):
            return self._choices

        return SmartLabelModelChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)


class JSONField(forms.CharField):
    def prepare_value(self, value):
        try:
            return json.dumps(value)
        except ValueError:
            return '{}'

    def to_python(self, value):
        try:
            return json.loads(value)
        except ValueError:
            return {}


class SelectClassesForm(forms.ModelForm):
    """Form for a parent to select classes for a kid."""
    when = JSONField(widget=forms.HiddenInput, required=False)
    classes = ClassSelectField(
        queryset=models.Class.objects.none(),
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
        right_session = Q(session=self.session)
        already_in = Q(pk__in=in_classes)
        valid = already_in
        if age is not None:
            age_match = Q(min_age__lte=age, max_age__gte=age)
            valid = valid | age_match
        valid_classes = models.Class.objects.annotate(
            num_students=Count('students'),
        ).filter(
            right_session & valid
        ).select_related(
            'teacher'
        )
        self.fields['classes'].queryset = valid_classes
        self.fields['classes'].initial = [c.pk for c in in_classes]

    def save(self, commit=True):
        models.Student.objects.filter(
            child=self.instance, klass__session=self.session).delete()
        when = self.cleaned_data['when']
        for klass in self.cleaned_data['classes']:
            timestamp = when.get(str(klass.id))
            if timestamp is None:
                signed_up = timezone.now()
            else:
                signed_up = datetime.fromtimestamp(
                    timestamp / 1000
                ).replace(tzinfo=timezone.get_current_timezone())
            models.Student.objects.get_or_create(
                child=self.instance, klass=klass, signed_up=signed_up)
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
