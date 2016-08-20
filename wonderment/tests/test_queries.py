import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'num_kids,cost',
    [
        (1, 135),
        (2, 135 + 95),
        (3, 135 + 95 + 55),
        (4, 135 + 95 + 55 + 25),
        (5, 135 + 95 + 55 + 25 + 25),
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
