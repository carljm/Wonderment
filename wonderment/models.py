from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from django.db import models

from . import fields, utils


def today():
    return date.today()


GROUPS = [
    ("Nursery", (0, (1, 5))),
    ("Toddler", ((1, 6), 2)),
    ("Preschool", (3, 4)),
    ("K-1", (5, 6)),
    ("Elementary", (7, 9)),
    ("Middle/High", (10, 15)),
]


PARTICIPATION_TYPES = [
    ('teaching', "teaching a class"),
    ('assisting', "assisting another teacher"),
    ('special', "helping to plan/facilitate special events / field trips"),
    ('policy', "review policy handbook and guidelines"),
    ('recruit', "publicity/recruitment"),
    ('sub', "being available as a substitute for teachers who are ill"),
    ('feedback', "collecting feedback from participants"),
    ('sub-coord', "substitute coordinator"),
    ('attendance', "monitor attendance"),
    ('volunteers', "thank yous / volunteer follow-up"),
    ('treasurer', "financial/treasury"),
    ('legal', "legal consultation"),
    ('conflict', "conflict management"),
    ('cleaning', "cleanup coordination"),
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
    participate_by = fields.ArrayField(
        verbose_name="How would you like to contribute to the co-op?",
        dbtype='text',
        choices=PARTICIPATION_TYPES,
    )
    age_groups = models.TextField(
        "Which age groups are you most comfortable working with? "
        "(Please note if you need to be with your own child's class.)",
        blank=True,
    )
    could_teach = models.TextField(
        "If you are interested in teaching, "
        "describe what you would like to teach.",
        blank=True,
    )
    could_assist = models.TextField(
        "What types of classes are you comfortable assisting with?",
        blank=True,
    )
    all_ages_help = models.TextField(
        "What ideas do you have for field trips or special events?",
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

    @property
    def participant_url(self):
        return reverse(
            'edit_participant_form',
            kwargs={'parent_id': self.id, 'id_hash': utils.idhash(self.id)},
        )

    @property
    def participate_by_display(self):
        for contribution in self.participate_by:
            val = PARTICIPATION_TYPE_MAP.get(contribution)
            if val:
                yield val

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

    def age_group(self, as_of):
        """Return name of age group this child is in."""
        age = self.age_delta(as_of, pretend=True)
        if age is not None:
            for group_name, (low, high) in GROUPS:
                low_months = 0
                high_months = 12
                if isinstance(low, tuple):
                    low, low_months = low
                if isinstance(high, tuple):
                    high, high_months = high
                if (
                        (age.years > low or (
                            age.years == low and age.months >= low_months))
                        and
                        (age.years < high or (
                            age.years == high and age.months <= high_months))
                ):
                    return group_name
        return None

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-birthdate']


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
        parents = []
        for p in participants:
            p.parent.jobs = p.jobs
            parents.append(p.parent)
        students = Child.objects.filter(parent__in=parents)
        age_groups_dict = {}
        for student in students:
            student.real_age = student.age_display(today())
            group = student.age_group(self.start_date)
            age_groups_dict.setdefault(group, []).append(student)
        age_groups = [
            (name, age_groups_dict[name])
            for name, ages in GROUPS
            if name in age_groups_dict
        ]
        if None in age_groups_dict:
            age_groups.append(("Unknown", age_groups_dict[None]))
        return {
            'parents': parents,
            'students': students,
            'grouped': age_groups,
        }


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
    )
    payment = models.CharField(
        max_length=20,
        choices=[
            (
                'early',
                "I am interested in discounted early registration. "
                "I understand that Wonderment cannot offer refunds. "
                "My family is committed to Wonderment participation "
                "to the best of our ability."
            ),
            (
                'later',
                "I would like to wait to complete my registration and payment."
            ),
        ],
    )
    paid = models.IntegerField(default=0)
    jobs = models.TextField(blank=True)

    def __str__(self):
        return "%s is %s for %s" % (self.parent, self.level, self.session)

    class Meta:
        ordering = ['parent__name']


class ClassDay(models.Model):
    session = models.ForeignKey(Session)
    date = models.DateField()

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ['-date']


class Attendance(models.Model):
    day = models.ForeignKey(ClassDay)
    child = models.ForeignKey(Child)
