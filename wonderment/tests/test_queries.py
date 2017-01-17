import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'committee,teacher,assisting,cleaning,num_kids,cost',
    [
        (False, False, False, False, 1, 125),
        (False, False, False, False, 2, 125 + 90),
        (False, False, False, False, 3, 125 + 90 + 50),
        (False, False, False, False, 4, 125 + 90 + 50 + 20),
        (False, False, False, False, 5, 125 + 90 + 50 + 20 + 20),
        # 50% discount for assisting
        (False, False, True, False, 1, 63),
        (False, False, True, False, 2, 108),
        # 20% discount for cleaning
        (False, False, False, True, 1, 100),
        (False, False, False, True, 2, 172),
        # discounts don't stack, just get the bigger one
        (False, False, True, True, 1, 63),
        (False, False, True, True, 2, 108),
        # committee members are free
        (True, False, False, False, 1, 0),
        # teachers are free
        (False, True, False, False, 1, 0),
    ],
)
def test_get_cost(db, committee, teacher, assisting, cleaning, num_kids, cost):
    volunteer = []
    if assisting:
        volunteer.append('assisting')
    if cleaning:
        volunteer.append('cleaning')
    p = f.ParticipantFactory.create(volunteer=volunteer)
    if committee:
        p.session.committee_members.add(p.parent)
    c1 = f.ClassFactory.create(session=p.session)
    if teacher:
        c1.teacher.parent = p.parent
        c1.teacher.save()
    c2 = f.ClassFactory.create(session=p.session)
    for i in range(num_kids):
        child = f.ChildFactory.create(parent=p.parent)
        f.StudentFactory.create(klass=c1, child=child)
        f.StudentFactory.create(klass=c2, child=child)

    assert queries.get_cost(p) == cost
