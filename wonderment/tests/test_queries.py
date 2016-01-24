import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'one_day_kids,two_day_kids,cost',
    [
        (1, 0, 115),
        (2, 0, 115 + 100),
        (3, 0, 115 + 100 + 85),
        (4, 0, 115 + 100 + 85 + 70),
        (5, 0, 115 + 100 + 85 + 70 + 70),
        (0, 1, 115 + 105),
        (0, 2, (115 + 105) + (100 + 90)),
        (0, 3, (115 + 105) + (100 + 90) + (85 + 75)),
        (0, 4, (115 + 105) + (100 + 90) + (85 + 75) + (70 + 60)),
        (0, 5, (115 + 105) + (100 + 90) + (85 + 75) + ((70 + 60) * 2)),
        (1, 1, (115 + 105) + 100),
        (1, 2, (115 + 105) + (100 + 90) + 85),
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
