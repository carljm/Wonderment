import json
from datetime import datetime

import floppyforms.__future__ as forms
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import (
    Count,
    Q,
)
from django.forms.models import (
    BaseInlineFormSet,
    ModelChoiceIterator,
    inlineformset_factory,
)
from django.template.loader import render_to_string
from django.utils import timezone

from . import (
    models,
    queries,
)


class WaiverForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = [
            'agreed_to_waiver'
        ]

    def __init__(self, *a, **kw):
        super(WaiverForm, self).__init__(*a, **kw)
        self.fields['agreed_to_waiver'].required = True


class DonationForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = [
            'donation'
        ]


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = [
            'volunteer',
        ]

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session')
        parent = kwargs.pop('parent')
        super(ParticipantForm, self).__init__(*args, **kwargs)
        for name, question in self.get_session_question_fields():
            self.fields[name] = question.formfield()
            if parent:
                answer = question.answers.filter(parent=parent).first()
                if answer:
                    response = answer.response
                    if question.question_type == 'checkbox':
                        response = True if response == 'True' else False
                    self.initial[name] = response

    def save(self, parent):
        participant = super(ParticipantForm, self).save(commit=False)
        participant.parent = parent
        participant.session = self.session
        self.save_session_question_answers(parent)
        participant.save()
        return participant

    def get_session_question_fields(self):
        questions = models.SessionQuestion.objects.filter(session=self.session)
        return [
            ('session-question-%s' % q.id, q)
            for q in questions
        ]

    def save_session_question_answers(self, parent):
        for name, question in self.get_session_question_fields():
            response = self.cleaned_data.get(name)
            models.SessionQuestionAnswer.objects.update_or_create(
                question=question,
                parent=parent,
                defaults={'response': response},
            )


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
            'pick_up_names',
            'future_job_interests',
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

    def send(self, session):
        for parent in self._parents:
            url = queries.get_idhash_url(
                'edit_participant_form', parent, session)
            context = {
                'parent': parent,
                'session': session,
                'edit_participant_url': settings.BASE_URL + url,
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

    def label_from_instance(self, obj):
        return "%s: %s (age %s-%s), %s: %s" % (
            obj.when,
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
