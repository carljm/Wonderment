from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil import rrule
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property

from . import fields, utils


def today():
    return date.today()


PARTICIPATION_TYPES = [
    ('coordination', "join the planning team (future session)"),
    ('teaching', "teaching a class (future session)"),
    ('assisting', "assisting another teacher"),
    ('sub', "available as a substitute for teachers who are ill"),
    ('cleaning', "cleaning"),
]


PARTICIPATION_TYPE_MAP = dict(PARTICIPATION_TYPES)


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
    pick_up_names = models.TextField(
        (
            "If dropping off, please list name, relationship, and contact "
            "for anyone authorized to pick up your child "
            "(or permission for child to transport themselves)."
        ),
        blank=True,
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
    participate_by = fields.ArrayField(
        verbose_name=(
            "I would be interested in helping out during Wonderment "
            "in one of the following ways for this or future sessions "
            "(check any that interest you):"
        ),
        dbtype='text',
        choices=PARTICIPATION_TYPES,
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

    @cached_property
    def participant_url(self):
        return reverse(
            'edit_participant_form',
            kwargs={'parent_id': self.id, 'id_hash': utils.idhash(self.id)},
        )

    @cached_property
    def select_classes_url(self):
        return reverse(
            'select_classes',
            kwargs={'parent_id': self.id, 'id_hash': utils.idhash(self.id)},
        )

    @cached_property
    def spring2015survey_url(self):
        return reverse(
            'spring2015survey',
            kwargs={'parent_id': self.id, 'id_hash': utils.idhash(self.id)},
        )

    @cached_property
    def fall2015eval_url(self):
        return reverse(
            'fall2015eval',
            kwargs={'parent_id': self.id, 'id_hash': utils.idhash(self.id)},
        )

    @cached_property
    def participate_by_display(self):
        return [PARTICIPATION_TYPE_MAP[c] for c in self.participate_by]

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
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date']

    def families(self, **filters):
        participants = self.participants.filter(
            paid__gt=0, **filters).select_related('parent')
        parents = [p.parent for p in participants]
        students = Child.objects.filter(parent__in=parents)
        for student in students:
            student.real_age = student.age_display(today())
        return {
            'parents': parents,
            'students': students,
        }


class Class(models.Model):
    WEEKDAYS = [
        (rrule.SU.weekday, "Sun"),
        (rrule.MO.weekday, "Mon"),
        (rrule.TU.weekday, "Tue"),
        (rrule.WE.weekday, "Wed"),
        (rrule.TH.weekday, "Thu"),
        (rrule.FR.weekday, "Fri"),
        (rrule.SA.weekday, "Sat"),
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
                    "to participation in Wonderment winter/spring 2016. "
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
                    "to participation in Wonderment this winter/spring 2016."
                ),
            ),
            (
                'not-ready',
                (
                    "I am not yet ready to make my payment. "
                    "I understand that class space "
                    "may be limited and that Wonderment "
                    "enrollment fees will increase after Feb 5, 2016. "
                ),
            ),
        ],
    )
    paid = models.IntegerField(default=0)
    assigned_jobs = fields.ArrayField(
        dbtype='text', choices=PARTICIPATION_TYPES)
    job_notes = models.TextField(blank=True)

    def __str__(self):
        return "%s is signed up for %s" % (self.parent, self.session)

    class Meta:
        ordering = ['parent__name']
        verbose_name = "participant in session"

    @cached_property
    def assigned_job_descs(self):
        return [PARTICIPATION_TYPE_MAP[j] for j in self.assigned_jobs]


class ClassDay(models.Model):
    session = models.ForeignKey(Session, related_name='classdays')
    date = models.DateField()

    def __str__(self):
        return self.date.strftime('%B %d, %Y')

    class Meta:
        ordering = ['-date']


ATTENDANCE = [
    ('present', 'present'),
    ('planned', 'absent (planned)'),
    ('short', 'absent (short notice)'),
    ('surprise', 'absent (no notice)'),
]


class ParentAttendance(models.Model):
    classday = models.ForeignKey(ClassDay)
    parent = models.ForeignKey(Parent)
    attendance = models.CharField(
        max_length=20, choices=ATTENDANCE, blank=True, null=True)


class ChildAttendance(models.Model):
    classday = models.ForeignKey(ClassDay)
    child = models.ForeignKey(Child)
    attendance = models.CharField(
        max_length=20, choices=ATTENDANCE, blank=True, null=True)
