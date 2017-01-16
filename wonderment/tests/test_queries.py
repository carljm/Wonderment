import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'assisting,cleaning,num_kids,cost',
    [
        (False, False, 1, 125),
        (False, False, 2, 125 + 90),
        (False, False, 3, 125 + 90 + 50),
        (False, False, 4, 125 + 90 + 50 + 20),
        (False, False, 5, 125 + 90 + 50 + 20 + 20),
        # 50% discount for assisting
        (True, False, 1, 63),
        (True, False, 2, 108),
        # 20% discount for cleaning
        (False, True, 1, 100),
        (False, True, 2, 172),
        # discounts don't stack, just get the bigger one
        (True, True, 1, 63),
        (True, True, 2, 108),
    ],
)
def test_get_cost(db, assisting, cleaning, num_kids, cost):
    volunteer = []
    if assisting:
        volunteer.append('assisting')
    if cleaning:
        volunteer.append('cleaning')
    p = f.ParticipantFactory.create(volunteer=volunteer)
    c1 = f.ClassFactory.create(session=p.session)
    c2 = f.ClassFactory.create(session=p.session)
    for i in range(num_kids):
        child = f.ChildFactory.create(parent=p.parent)
        f.StudentFactory.create(klass=c1, child=child)
        f.StudentFactory.create(klass=c2, child=child)

    assert queries.get_cost(p) == cost
