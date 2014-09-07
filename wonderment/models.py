from dateutil.relativedelta import relativedelta
from django.db import models


GROUPS = [
    ("Toddler", (1, 2)),
    ("Pre-1", (3, 6)),
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
    participate_by = models.TextField(blank=True)
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
    pretend_birthdate = models.DateField(blank=True, null=True)
    special_needs = models.TextField(blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'male'), ('female', 'female')],
        blank=True,
    )

    def age(self, as_of):
        """Return age as relativedelta."""
        bd = (self.pretend_birthdate or self.birthdate)
        if bd:
            return relativedelta(as_of, bd)
        return None

    def age_years(self, as_of):
        age = self.age(as_of)
        if age is not None:
            return age.years
        return None

    def age_group(self, as_of):
        """Return name of age group this child is in."""
        age = self.age_years(as_of)
        if age is not None:
            for group_name, (low, high) in GROUPS:
                if age >= low and age <= high:
                    return group_name
        return None

    def __str__(self):
        return self.name

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
