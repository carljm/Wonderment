import datetime

import factory

from wonderment.models import (
    Parent, Child, Session, Participant, ClassDay)


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
        model = Parent

    name = "Test Parent"


class ChildFactory(ModelFactory):
    class Meta:
        model = Child

    parent = factory.SubFactory(ParentFactory)
    name = "Test Child"


class SessionFactory(ModelFactory):
    class Meta:
        model = Session

    name = "Test Session"
    start_date = datetime.date(2014, 9, 12)
    end_date = datetime.date(2014, 12, 5)


class ParticipantFactory(ModelFactory):
    class Meta:
        model = Participant

    parent = factory.SubFactory(ParentFactory)
    session = factory.SubFactory(SessionFactory)
    level = 'weekly'


class ClassDayFactory(ModelFactory):
    class Meta:
        model = ClassDay

    session = factory.SubFactory(SessionFactory)
    date = datetime.date(2014, 9, 12)
