from django.db import models


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

    def __str__(self):
        return self.name


class Child(models.Model):
    parent = models.ForeignKey(Parent)
    name = models.CharField(max_length=200)
    birthdate = models.DateField(blank=True)
    special_needs = models.TextField()
    gender = models.CharField(
        max_length=1, choices=[('male', 'male'), ('female', 'female')])

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Participant(models.Model):
    parent = models.ForeignKey(Parent)
    session = models.ForeignKey(Session)
    level = models.CharField(
        max_length=20, choices=[('weekly', 'weekly'), ('monthly', 'monthly')])
    paid = models.IntegerField(default=0)
    jobs = models.TextField(blank=True)

    def __str__(self):
        return "%s is %s for %s" % (self.parent, self.level, self.session)
