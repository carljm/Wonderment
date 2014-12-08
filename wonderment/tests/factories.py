import datetime

import factory

from wonderment.models import (
    Parent, Child, Session, Participant, ClassDay, Attendance)


class ModelFactory(factory.DjangoModelFactory):
    """We don't want to go to the database to get the next sequence value."""
    ABSTRACT_FACTORY = True

    @classmethod
    def _setup_next_sequence(cls):
        """Set up an initial sequence value for Sequence attributes."""
        return 0


class ParentFactory(ModelFactory):
    FACTORY_FOR = Parent

    name = "Test Parent"


class ChildFactory(ModelFactory):
    FACTORY_FOR = Child

    parent = factory.SubFactory(ParentFactory)
    name = "Test Child"


class SessionFactory(ModelFactory):
    FACTORY_FOR = Session

    name = "Test Session"
    start_date = datetime.date(2014, 9, 12)
    end_date = datetime.date(2014, 12, 5)


class ParticipantFactory(ModelFactory):
    FACTORY_FOR = Participant

    parent = factory.SubFactory(ParentFactory)
    session = factory.SubFactory(SessionFactory)
    level = 'weekly'
    payment = 'early'


class ClassDayFactory(ModelFactory):
    FACTORY_FOR = ClassDay

    session = factory.SubFactory(SessionFactory)
    date = datetime.date(2014, 9, 12)


class AttendanceFactory(ModelFactory):
    FACTORY_FOR = Attendance

    day = factory.SubFactory(ClassDayFactory)
    child = factory.SubFactory(ChildFactory)
