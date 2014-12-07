from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models


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


class Parent(models.Model):
    name = models.CharField(max_length=200)
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
    spouse = models.CharField(max_length=200, blank=True)
    spouse_contact = models.CharField(max_length=200, blank=True)
    emergency = models.CharField(max_length=200, blank=True)
    emergency_contact = models.CharField(max_length=200, blank=True)
    age_groups = models.TextField(blank=True)
    could_teach = models.TextField(blank=True)
    could_assist = models.TextField(blank=True)
    all_ages_help = models.TextField(blank=True)
    other_contributions = models.TextField(blank=True)
    classes_desired = models.TextField(blank=True)

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
    special_needs = models.TextField(blank=True)
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
        max_length=20, choices=[('weekly', 'weekly'), ('monthly', 'monthly')])
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
