import factory

from wonderment.models import Parent, Child, Session, Participant


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


class ParticipantFactory(ModelFactory):
    FACTORY_FOR = Participant

    parent = factory.SubFactory(ParentFactory)
    session = factory.SubFactory(SessionFactory)
    level = 'weekly'
