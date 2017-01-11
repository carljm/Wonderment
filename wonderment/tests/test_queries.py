import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'assisting,num_kids,cost',
    [
        (False, 1, 125),
        (False, 2, 125 + 90),
        (False, 3, 125 + 90 + 50),
        (False, 4, 125 + 90 + 50 + 20),
        (False, 5, 125 + 90 + 50 + 20 + 20),
        (True, 1, 63),
        (True, 2, 108),
    ],
)
def test_get_cost(db, assisting, num_kids, cost):
    volunteer = ['assisting'] if assisting else []
    p = f.ParticipantFactory.create(volunteer=volunteer)
    c1 = f.ClassFactory.create(session=p.session)
    c2 = f.ClassFactory.create(session=p.session)
    for i in range(num_kids):
        child = f.ChildFactory.create(parent=p.parent)
        f.StudentFactory.create(klass=c1, child=child)
        f.StudentFactory.create(klass=c2, child=child)

    assert queries.get_cost(p) == cost
