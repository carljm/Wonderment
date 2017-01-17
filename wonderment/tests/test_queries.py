import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'donation,paid,committee,teacher,assist,sub,cleaning,num_kids,breakdown',
    [
        (
            0, 0, False, False, False, False, False, 1,
            {
                'costs': [("First kid", 125)],
                'total': 125,
                'paid': 0,
                'owed': 125,
            }
        ),
        (
            0, 0, False, False, False, False, False, 2,
            {
                'costs': [
                    ("First kid", 125),
                    ("Second kid", 90),
                ],
                'total': 215,
                'paid': 0,
                'owed': 215,
            }
        ),
        (
            0, 0, False, False, False, False, False, 3,
            {
                'costs': [
                    ("First kid", 125),
                    ("Second kid", 90),
                    ("Third kid", 50),
                ],
                'total': 265,
                'paid': 0,
                'owed': 265,
            }
        ),
        (
            0, 0, False, False, False, False, False, 4,
            {
                'costs': [
                    ("First kid", 125),
                    ("Second kid", 90),
                    ("Third kid", 50),
                    ("Fourth kid", 20),
                ],
                'total': 285,
                'paid': 0,
                'owed': 285,
            }
        ),
        (
            0, 0, False, False, False, False, False, 5,
            {
                'costs': [
                    ("First kid", 125),
                    ("Second kid", 90),
                    ("Third kid", 50),
                    ("Fourth kid", 20),
                    ("Fifth kid", 20),
                ],
                'total': 305,
                'paid': 0,
                'owed': 305,
            }
        ),
        # 50% discount for assisting
        (
            0, 0, False, False, True, False, False, 1,
            {
                'costs': [
                    ("First kid", 125),
                    ("50% assistant discount", -62),
                ],
                'total': 63,
                'paid': 0,
                'owed': 63,
            }
        ),
        # 25% discount for subbing
        (
            0, 0, False, False, False, True, False, 1,
            {
                'costs': [
                    ("First kid", 125),
                    ("25% sub discount", -31),
                ],
                'total': 94,
                'paid': 0,
                'owed': 94,
            }
        ),
        # 20% discount for cleaning
        (
            0, 0, False, False, False, False, True, 1,
            {
                'costs': [
                    ("First kid", 125),
                    ("20% cleaning discount", -25),
                ],
                'total': 100,
                'paid': 0,
                'owed': 100,
            }
        ),
        # discounts don't stack, just get the bigger one
        (
            0, 0, False, False, True, False, True, 1,
            {
                'costs': [
                    ("First kid", 125),
                    ("50% assistant discount", -62),
                ],
                'total': 63,
                'paid': 0,
                'owed': 63,
            }
        ),
        # committee members are free
        (
            0, 0, True, False, False, False, False, 1,
            {
                'costs': [
                    ("First kid", 125),
                    ("100% committee discount", -125),
                ],
                'total': 0,
                'paid': 0,
                'owed': 0,
            }
        ),
        # teachers are free
        (
            0, 0, False, True, False, False, False, 1,
            {
                'costs': [
                    ("First kid", 125),
                    ("Teacher (cost deducted from pay)", -125),
                ],
                'total': 0,
                'paid': 0,
                'owed': 0,
            }
        ),
        # donation is included
        (
            75, 0, False, False, False, False, False, 1,
            {
                'costs': [
                    ("First kid", 125),
                    ("Donation", 75),
                ],
                'total': 200,
                'paid': 0,
                'owed': 200,
            }
        ),
        # already-paid is deducated
        (
            0, 100, False, False, False, False, False, 1,
            {
                'costs': [("First kid", 125)],
                'total': 125,
                'paid': 100,
                'owed': 25,
            }
        ),
    ],
)
def test_get_bill(
        db,
        donation, paid, committee, teacher, assist, sub, cleaning, num_kids,
        breakdown
):
    volunteer = []
    if assist:
        volunteer.append('assisting')
    if sub:
        volunteer.append('sub')
    if cleaning:
        volunteer.append('cleaning')
    p = f.ParticipantFactory.create(
        volunteer=volunteer, donation=donation, paid=paid)
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

    assert queries.get_bill(p) == breakdown
