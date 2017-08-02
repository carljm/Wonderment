import pytest

from wonderment import queries
from wonderment.tests import factories as f


@pytest.mark.parametrize(
    'donation,paid,committee,teacher,num_kids,breakdown',
    [
        (
            0, 0, False, False, 1,
            {
                'costs': [("1 student x $30", 30)],
                'total': 30,
                'paid': 0,
                'owed': 30,
            }
        ),
        (
            0, 0, False, False, 2,
            {
                'costs': [
                    ("2 students x $30", 60),
                ],
                'total': 60,
                'paid': 0,
                'owed': 60,
            }
        ),
        # committee members are free
        (
            0, 0, True, False, 1,
            {
                'costs': [
                    ("1 student x $30", 30),
                    ("100% committee discount", -30),
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
                    ("1 student x $30", 30),
                    ("Teacher (cost deducted from pay)", -30),
                ],
                'total': 0,
                'paid': 0,
                'owed': 0,
            }
        ),
        # donation is included
        (
            70, 0, False, False, 1,
            {
                'costs': [
                    ("1 student x $30", 30),
                    ("Donation", 70),
                ],
                'total': 100,
                'paid': 0,
                'owed': 100,
            }
        ),
        # already-paid is deducted
        (
            0, 10, False, False, 1,
            {
                'costs': [("1 student x $30", 30)],
                'total': 30,
                'paid': 10,
                'owed': 20,
            }
        ),
    ],
)
def test_get_bill(db, donation, paid, committee, teacher, num_kids, breakdown):
    volunteer = []
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
