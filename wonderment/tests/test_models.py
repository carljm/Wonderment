from datetime import date

from dateutil.relativedelta import relativedelta

from wonderment.tests import factories as f


class TestChild(object):
    def test_age(self):
        c = f.ChildFactory.build(birthdate=date(2014, 9, 1))

        assert c.age(date(2014, 9, 6)) == relativedelta(days=5)

    def test_age_group(self):
        c = f.ChildFactory.build(birthdate=date(2006, 9, 5))

        assert c.age_group(date(2014, 9, 6)) == "Elementary"

    def test_age_group_months(self):
        one = f.ChildFactory.build(birthdate=date(2013, 6, 1))
        two = f.ChildFactory.build(birthdate=date(2013, 1, 1))

        today = date(2014, 9, 6)
        assert one.age_group(today) == "Nursery"
        assert two.age_group(today) == "Toddler"
