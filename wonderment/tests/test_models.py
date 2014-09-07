from datetime import date

from dateutil.relativedelta import relativedelta

from wonderment.tests import factories as f


class TestChild(object):
    def test_age(self):
        c = f.ChildFactory.build(birthdate=date(2014, 9, 1))

        assert c.age(date(2014, 9, 6)) == relativedelta(days=5)

    def test_age_group(self):
        c = f.ChildFactory.build(birthdate=date(2012, 9, 5))

        assert c.age_group(date(2014, 9, 6)) == "Toddler"
