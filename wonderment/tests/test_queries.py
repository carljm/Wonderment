import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'donation,paid,committee,teacher,num_kids,breakdown',
    [
        (
            0, 0, False, False, 1,
            {
                'costs': [("First kid", 85)],
                'total': 85,
                'paid': 0,
                'owed': 85,
            }
        ),
        (
            0, 0, False, False, 2,
            {
                'costs': [
                    ("First kid", 85),
                    ("Second kid", 85),
                ],
                'total': 170,
                'paid': 0,
                'owed': 170,
            }
        ),
        # committee members are free
        (
            0, 0, True, False, 1,
            {
                'costs': [
                    ("First kid", 85),
                    ("100% committee discount", -85),
                ],
                'total': 0,
                'paid': 0,
                'owed': 0,
            }
        ),
        # teachers are free
        (
            0, 0, False, True, 1,
            {
                'costs': [
                    ("First kid", 85),
                    ("Teacher (cost deducted from pay)", -85),
                ],
                'total': 0,
                'paid': 0,
                'owed': 0,
            }
        ),
        # donation is included
        (
            75, 0, False, False, 1,
            {
                'costs': [
                    ("First kid", 85),
                    ("Donation", 75),
                ],
                'total': 160,
                'paid': 0,
                'owed': 160,
            }
        ),
        # already-paid is deducated
        (
            0, 60, False, False, 1,
            {
                'costs': [("First kid", 85)],
                'total': 85,
                'paid': 60,
                'owed': 25,
            }
        ),
    ],
)
def test_get_bill(db, donation, paid, committee, teacher, num_kids, breakdown):
    p = f.ParticipantFactory.create(donation=donation, paid=paid)
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
