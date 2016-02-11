import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'one_day_kids,two_day_kids,cost',
    [
        (1, 0, 125),
        (2, 0, 125 + 110),
        (3, 0, 125 + 110),
        (4, 0, 125 + 110),
        (5, 0, 125 + 110),
        (0, 1, 125 + 115),
        (0, 2, (125 + 115) + (110 + 100)),
        (0, 3, (125 + 115) + (110 + 100)),
        (0, 4, (125 + 115) + (110 + 100)),
        (0, 5, (125 + 115) + (110 + 100)),
        (1, 1, (125 + 115) + 110),
        (1, 2, (125 + 115) + (110 + 100)),
    ],
)
def test_get_cost(db, one_day_kids, two_day_kids, cost):
    p = f.ParticipantFactory.create()
    c1 = f.ClassFactory.create(weekday=0, session=p.session)
    c2 = f.ClassFactory.create(weekday=1, session=p.session)
    for i in range(one_day_kids):
        f.StudentFactory.create(klass=c1, child__parent=p.parent)
    for i in range(two_day_kids):
        student = f.StudentFactory.create(klass=c1, child__parent=p.parent)
        f.StudentFactory.create(klass=c2, child=student.child)

    assert queries.get_cost(p.parent, p.session) == cost
