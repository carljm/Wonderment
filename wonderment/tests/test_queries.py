import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'num_kids,cost',
    [
        (1, 125),
        (2, 125 + 90),
        (3, 125 + 90 + 50),
        (4, 125 + 90 + 50 + 20),
        (5, 125 + 90 + 50 + 20 + 20),
    ],
)
def test_get_cost(db, num_kids, cost):
    p = f.ParticipantFactory.create()
    c1 = f.ClassFactory.create(session=p.session)
    c2 = f.ClassFactory.create(session=p.session)
    for i in range(num_kids):
        child = f.ChildFactory.create(parent=p.parent)
        f.StudentFactory.create(klass=c1, child=child)
        f.StudentFactory.create(klass=c2, child=child)

    assert queries.get_cost(p.parent, p.session) == cost
