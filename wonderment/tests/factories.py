import datetime

import factory

from wonderment import models


class ModelFactory(factory.DjangoModelFactory):
    """We don't want to go to the database to get the next sequence value."""
    class Meta:
        abstract = True

    @classmethod
    def _setup_next_sequence(cls):
        """Set up an initial sequence value for Sequence attributes."""
        return 0


class ParentFactory(ModelFactory):
    class Meta:
        model = models.Parent

    name = "Test Parent"


class ChildFactory(ModelFactory):
    class Meta:
        model = models.Child

    parent = factory.SubFactory(ParentFactory)
    name = "Test Child"


class SessionFactory(ModelFactory):
    class Meta:
        model = models.Session

    name = "Test Session"
    start_date = datetime.date(2014, 9, 12)
    end_date = datetime.date(2014, 12, 5)


class ParticipantFactory(ModelFactory):
    class Meta:
        model = models.Participant

    parent = factory.SubFactory(ParentFactory)
    session = factory.SubFactory(SessionFactory)


class TeacherFactory(ModelFactory):
    class Meta:
        model = models.Teacher

    name = "Test Teacher"


class ClassFactory(ModelFactory):
    class Meta:
        model = models.Class

    teacher = factory.SubFactory(TeacherFactory)
    session = factory.SubFactory(SessionFactory)
    name = "Test Class"
    min_age = 1
    max_age = 5
    max_students = 10
    weekday = 1
    start = datetime.time(9, 15)
    end = datetime.time(10, 15)


class StudentFactory(ModelFactory):
    class Meta:
        model = models.Student

    child = factory.SubFactory(ChildFactory)
    klass = factory.SubFactory(ClassFactory)
    signed_up = datetime.datetime(2016, 1, 22, 20, 15)


class ClassDayFactory(ModelFactory):
    class Meta:
        model = models.ClassDay

    session = factory.SubFactory(SessionFactory)
    date = datetime.date(2014, 9, 12)
