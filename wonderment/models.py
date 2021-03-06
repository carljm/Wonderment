from datetime import date

import floppyforms.__future__ as forms
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils.functional import cached_property

from . import fields


def today():
    return date.today()


JOBS = [
    ('assisting', "assisting a teacher"),
    ('sub', "being available as a substitute for teachers who are ill"),
    ('cleaning', "cleaning up after classes"),
]


JOBS_MAP = dict(JOBS)


FUTURE_JOBS = [
    ('coordination', "joining the planning team"),
    ('teaching', "teaching a class"),
]


class Parent(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=25)
    phone_type = models.CharField(
        max_length=20,
        choices=[
            ('cell', 'cell'),
            ('home', 'home'),
            ('work', 'work'),
        ],
        blank=True,
    )
    email = models.EmailField()
    address = models.CharField(max_length=300, blank=True)
    preferred = models.CharField(
        max_length=20,
        choices=[
            ('email', 'email'),
            ('phone', 'phone'),
            ('text', 'text'),
            ('facebook', 'facebook'),
        ],
        blank=True,
        )
    spouse = models.CharField("Spouse name", max_length=200, blank=True)
    spouse_contact = models.CharField(max_length=200, blank=True)
    emergency = models.CharField(
        "Emergency contact name", max_length=200, blank=True)
    emergency_contact = models.CharField(
        "Emergency contact number", max_length=200, blank=True)
    pick_up_names = models.TextField(
        (
            "If dropping off, please list name, relationship, and contact "
            "for anyone authorized to pick up your child "
            "(or permission for child to transport themselves)."
        ),
        blank=True,
    )
    future_job_interests = fields.ArrayChoiceField(
        models.TextField(choices=FUTURE_JOBS),
        verbose_name="For future sessions, I am interested in possibly:",
        blank=True,
        default=list,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Child(models.Model):
    parent = models.ForeignKey(Parent, related_name='children')
    name = models.CharField(max_length=200)
    birthdate = models.DateField(blank=True, null=True)
    birthdate_approx = models.BooleanField(default=False)
    pretend_birthdate = models.DateField(blank=True, null=True)
    special_needs = models.TextField(
        "Special needs, if any (potty training, allergies)",
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'male'), ('female', 'female')],
        blank=True,
    )

    @property
    def real_age(self):
        return self.age_display(today())

    def age_delta(self, as_of, pretend=False):
        """Return age as relativedelta."""
        bd = self.birthdate
        if pretend and self.pretend_birthdate:
            bd = self.pretend_birthdate
        if bd:
            return relativedelta(as_of, bd)
        return None

    def age_years(self, as_of):
        age = self.age_delta(as_of)
        if age is not None:
            return age.years
        return None

    def age_display(self, as_of):
        age = self.age_delta(as_of)
        if age is not None:
            if age.years < 1 and age.months < 1:
                return "%swk" % int(age.days / 7)
            if age.years < 2:
                months = (age.years * 12) + age.months
                return "%smo" % months
            return "%syr" % age.years
        return "?"

    def sign_in_status(self, as_of):
        last_xfer = self.transfers.order_by('-timestamp').first()
        if last_xfer is None:
            return 'none'
        elif last_xfer.timestamp.date() < as_of:
            return 'stale' if last_xfer.in_out == 'in' else 'none'
        return last_xfer.in_out

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-birthdate']
        verbose_name_plural = "children"


class Teacher(models.Model):
    name = models.CharField(max_length=100, blank=True)
    parent = models.OneToOneField(Parent, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True)
    phone_type = models.CharField(
        max_length=20,
        choices=[
            ('cell', 'cell'),
            ('home', 'home'),
            ('work', 'work'),
        ],
        blank=True,
    )
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    preferred = models.CharField(
        max_length=20,
        choices=[
            ('email', 'email'),
            ('phone', 'phone'),
            ('text', 'text'),
            ('facebook', 'facebook'),
        ],
        blank=True,
        )
    bio = models.TextField(blank=True)
    class_ideas = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *a, **kw):
        if self.parent:
            self.name = self.parent.name
            self.phone = self.parent.phone
            self.phone_type = self.parent.phone_type
            self.email = self.parent.email
            self.address = self.parent.address
            self.preferred = self.parent.preferred
        return super(Teacher, self).save(*a, **kw)

    class Meta:
        ordering = ['name']


class Session(models.Model):
    name = models.CharField(max_length=100)
    registration_opens = models.DateTimeField()
    registration_closes = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    confirm_email = models.TextField(
        help_text=(
            "Full text of confirmation email sent after payment is completed. "
            "Use {{ parent }} for the parent's name, "
            "{{ session }} for the name of the session, {{ payment_url }} "
            "for the payment URL to visit if more payment is needed, "
            "{{ bill.paid }} for the amount they have already paid, "
            "{{ bill.total }} for their total cost, {{ bill.owed }} "
            "for any remaining amount owed, "
            "{{ bill_summary }} for an itemized listing, and "
            "{{ children_and_classes }} for a full list of children/classes."
        ),
        default=(
            "{{ parent }},\n\n"
            "We've received your registration "
            "for Wonderment {{ session }}!\n\n"
            "{% if bill.paid %}"
            "Thanks for your payment of ${{ bill.paid }}.\n"
            "{% endif %}"
            "{% if bill.owed %}\n"
            "Your registration and class selections "
            "will not be confirmed until you pay the remaining amount "
            "of ${{ bill.owed }}. Please visit {{ payment_url }} to complete "
            "your registration as soon as possible.\n"
            "{% else %}\n"
            "Your registration is fully paid and confirmed, thank you!\n"
            "Your children are signed up for the following classes:\n\n"
            "{{ children_and_classes }}\n\n"
            "{% endif %}\n"
            "Your cost and payment summary:\n"
            "{{ bill_summary }}\n"
            "-- Wonderment Team"
        ),
    )
    registrar_email_address = models.EmailField(
        default='registrar@wondermentblackhills.com')
    online_payment = models.BooleanField(default=True)
    waiver = models.TextField(blank=True)
    committee_members = models.ManyToManyField(
        Parent, related_name='committee_for_sessions', blank=True)
    payment_extra_info = models.TextField(blank=True)
    donation_text = models.TextField(
        default="Please consider adding a donation to your registration!")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date']

    def families(self):
        participants = self.participants.filter(
            paid__gt=0
        ).select_related('parent')
        parents = [p.parent for p in participants]
        students = Child.objects.filter(parent__in=parents)
        return {
            'parents': parents,
            'students': students,
        }


class SessionQuestion(models.Model):
    session = models.ForeignKey(Session, related_name='questions')
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('checkbox', 'checkbox'),
            ('line', 'line'),
            ('paragraph', 'paragraph'),
        ],
    )
    text = models.TextField()
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['session', 'order']

    def __str__(self):
        return "(%s) %s" % (self.session, self.text)

    def formfield(self):
        field_class, widget_class = {
            'checkbox': (forms.BooleanField, forms.CheckboxInput),
            'line': (forms.CharField, forms.TextInput),
            'paragraph': (forms.CharField, forms.Textarea),
        }[self.question_type]
        return field_class(
            label=self.text, widget=widget_class(), required=self.required)


class SessionQuestionAnswer(models.Model):
    question = models.ForeignKey(SessionQuestion, related_name='answers')
    parent = models.ForeignKey(Parent)
    response = models.TextField()

    class Meta:
        unique_together = [('question', 'parent')]

    def __str__(self):
        return self.response


class Class(models.Model):
    WEEKDAYS = [
        (rrule.SU.weekday, "Sun"),
        (rrule.MO.weekday, "Mon"),
        (rrule.TU.weekday, "Tue"),
        (rrule.WE.weekday, "Wed"),
        (rrule.TH.weekday, "Thu"),
        (rrule.FR.weekday, "Fri"),
        (rrule.SA.weekday, "Sat"),
        (99, "Wed/Thu/Fri"),
    ]

    teacher = models.ForeignKey(Teacher, related_name='classes')
    session = models.ForeignKey(Session, related_name='classes')
    name = models.CharField(max_length=100)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    max_students = models.IntegerField()
    weekday = models.IntegerField(choices=WEEKDAYS)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['session', 'weekday', 'start']
        verbose_name_plural = 'classes'

    @cached_property
    def when(self):
        start_ap = self.start.strftime('%p').lower()
        end_ap = self.end.strftime('%p').lower()
        if start_ap == end_ap:
            start_ap = ''
        start_mins = self.start.strftime('%M')
        if start_mins == '00':
            start_mins = ''
        else:
            start_mins = ':' + start_mins
        end_mins = self.end.strftime('%M')
        if end_mins == '00':
            end_mins = ''
        else:
            end_mins = ':' + end_mins
        return "%s %s%s%s-%s%s%s" % (
            self.get_weekday_display(),
            self.start.strftime('%-I'),
            start_mins,
            start_ap,
            self.end.strftime('%-I'),
            end_mins,
            end_ap,
        )


class Student(models.Model):
    child = models.ForeignKey(Child, related_name='studies')
    klass = models.ForeignKey(Class, related_name='students')
    signed_up = models.DateTimeField()

    def __str__(self):
        return "%s in %s" % (self.child, self.klass)

    class Meta:
        ordering = ['signed_up']


class Participant(models.Model):
    parent = models.ForeignKey(Parent, related_name='participations')
    session = models.ForeignKey(Session, related_name='participants')
    paid = models.IntegerField(default=0)
    volunteer = fields.ArrayChoiceField(
        models.TextField(choices=JOBS),
        verbose_name=(
            "I am interested in helping out this session by (optional):"),
        blank=True,
        default=list,
    )
    agreed_to_waiver = models.BooleanField(
        "I agree to the terms of the above waiver",
        default=False,
    )
    assigned_jobs = fields.ArrayChoiceField(
        models.TextField(choices=JOBS),
        blank=True,
        default=list,
    )
    notes = models.TextField(blank=True)
    donation = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s is signed up for %s" % (self.parent, self.session)

    class Meta:
        ordering = ['parent__name']
        verbose_name = "participant in session"


class ChildTransfer(models.Model):
    """Child sign in/out event."""
    IN = 'in'
    OUT = 'out'
    TRANSFER_TYPES = [
        (IN, 'sign in'),
        (OUT, 'sign out'),
    ]
    child = models.ForeignKey(Child, related_name='transfers')
    in_out = models.CharField(max_length=10, choices=TRANSFER_TYPES)
    initials = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def __str__(self):
        return "%s signed %s by %s at %s" % (
            self.child, self.in_out, self.initials,
            self.timestamp.strftime('%c')
        )

# Archives (ignore) #######


PARTICIPATION_TYPES = [
    ('coordination', "join the planning team (future session)"),
    ('teaching', "teaching a class (future session)"),
    ('assisting', "assisting another teacher"),
    ('sub', "available as a substitute for teachers who are ill"),
    ('cleaning', "cleaning"),
]


EXTENSION_HELP = [
    ('wed-class', "helping out during class as needed each Wed"),
    ('thu-class', "helping out during class as needed each Thu"),
    ('fri-class', "helping out during class as needed each Fri"),
    ('wed-clean', "staying late and helping clean up each Wed"),
    ('thu-clean', "staying late and helping clean up each Thu"),
    ('fri-clean', "staying late and helping clean up each Fri"),
    ('younger-sub', "substitute teaching for the Outdoor Immersion Program"),
    ('older-sub', "substitute teaching for the Project-Based Teamwork Class"),
]


class ParentArchive(models.Model):
    """Saving values of old, deprecated Parent fields."""
    parent = models.OneToOneField(Parent)
    drop_off = models.BooleanField(
        (
            "I am interested in the option to drop off my children "
            "for Wonderment classes.  I understand that I may be asked "
            "to remain on-site if behavioral issues, potty-training, "
            "or separation anxiety are a problem. I understand that I "
            "may lose the drop-off option if I fail to pick my child up "
            "before 11:35am from class and will also be charged a late "
            "pick-up fee. I understand that if my child is under four, "
            "I should be prepared to remain on-site for their first "
            "Wonderment class to make sure there are no issues with "
            "potty-training or separation anxiety."
        ),
        default=False,
    )
    on_site = models.BooleanField(
        (
            "I am interested in staying on-site during class "
            "either to observe my child's classroom "
            "or to be outside the classroom "
            "doing something of my own choosing "
            "or visiting with other parents."
        ),
        default=False,
    )
    participate_by = fields.ArrayChoiceField(
        models.TextField(choices=PARTICIPATION_TYPES),
        verbose_name=(
            "I would be interested in helping out during Wonderment "
            "in one of the following ways for this or future sessions "
            "(check any that interest you):"
        ),
    )
    could_teach = models.TextField(
        (
            "If you are interested in teaching, "
            "describe what you would like to teach, "
            "and to which age groups "
            "(probably for a future session):"
        ),
        blank=True,
    )
    could_assist = models.TextField(
        (
            "If interested in assisting, "
            "any preferences or considerations we should know about?"
        ),
        blank=True,
    )
    other_contributions = models.TextField(
        "Other ideas, suggestions, or contributions?",
        blank=True,
    )
    classes_desired = models.TextField(
        "Any particular subjects you hope will be offered?",
        blank=True,
    )

    def __str__(self):
        return "Archive for %s" % self.parent


class ParticipantArchive(models.Model):
    """Saving old values of deprecated Participant fields."""
    participant = models.OneToOneField(Participant)
    drop_off = models.BooleanField(
        (
            "I would like to drop off my children for Wonderment "
            "Extension classes.  I understand that I may be asked "
            "to remain on-site if behavioral issues, potty-training, "
            "or separation anxiety are a problem. I understand that I "
            "may lose the drop-off option if I fail to pick my child up "
            "on time from class and will also be charged a late "
            "pick-up fee. I understand that if my child is under four, "
            "I should be prepared to remain on-site for their first "
            "Wonderment Extension class to make sure there are no issues with "
            "potty-training or separation anxiety."
        ),
        default=False,
    )
    help_how = fields.ArrayChoiceField(
        models.TextField(choices=EXTENSION_HELP),
        verbose_name=(
            "I am able to help out during Wonderment Extension by:"
        ),
    )
    ideas = models.TextField("Questions, concerns, ideas:", blank=True)
    payment_amount = models.IntegerField(
        (
            "At this time, Wonderment Extension is running on a sliding "
            "scale per family monthly donation. Please fill in the amount "
            "you are able to pay monthly to Wonderment Extension, $20-200 "
            "per month per family (enter number only):"
        ),
    )
    absences = models.TextField(
        (
            "Please list dates of any planned absences. Fall session begins "
            "Thu Sept 22 (first week is Thu only), with regular classes "
            "9am-12pm W/Th/F Sept 28 - Dec 9, with a break Nov 23-25."
        ),
        blank=True,
    )
    part_time = models.TextField(
        (
            "If you will not be attending all three days of the week (W/Th/F),"
            " please note which weekday(s) you will attend."
        ),
        blank=True,
    )
    level = models.CharField(
        "I am signing my children up for:",
        max_length=20,
        choices=[
            ('weekly', 'all weekly classes'),
            ('monthly', 'only special events and field trips')
        ],
        default='weekly',
    )
    payment = models.CharField(
        max_length=20,
        choices=[
            (
                'ready',
                (
                    "My family is ready to commit "
                    "to participation in Wonderment fall 2016. "
                    "We understand that registration fees "
                    "are non-refundable."
                ),
            ),
            (
                'wait-for-role',
                (
                    "I will wait to make my payment "
                    "until I know for sure "
                    "if I will be assigned to a role "
                    "that would help off-set my tuition fees. "
                    "My family is otherwise committed "
                    "to participation in Wonderment this fall 2016."
                ),
            ),
            (
                'not-ready',
                (
                    "I am not yet ready to make my payment. "
                    "I understand that class space "
                    "may be limited."
                ),
            ),
        ],
    )
    assigned_jobs = fields.ArrayChoiceField(
        models.TextField(choices=PARTICIPATION_TYPES))
    job_notes = models.TextField(blank=True)

    def __str__(self):
        return "Archive for %s" % self.participant
