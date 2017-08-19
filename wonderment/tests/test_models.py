from datetime import datetime, date

from dateutil.relativedelta import relativedelta
import pytz

from wonderment.tests import factories as f


class TestParent:
    def test_str(self):
        assert str(f.ParentFactory.build(name="Foo")) == "Foo"


class TestChild:
    def test_str(self):
        assert str(f.ChildFactory.build(name="Foo")) == "Foo"

    def test_age_delta(self):
        c = f.ChildFactory.build(birthdate=date(2014, 9, 1))

        assert c.age_delta(date(2014, 9, 6)) == relativedelta(days=5)

    def test_age_delta_pretend(self):
        c = f.ChildFactory.build(
            birthdate=date(2014, 9, 1), pretend_birthdate=date(2014, 9, 3))

        assert c.age_delta(date(2014, 9, 6), pretend=True) == relativedelta(
            days=3)

    def test_age_delta_none(self):
        c = f.ChildFactory.build(birthdate=None, pretend_birthdate=None)

        assert c.age_delta(date(2014, 9, 6)) is None

    def test_age_years(self):
        c = f.ChildFactory.build(birthdate=date(2011, 9, 1))

        assert c.age_years(date(2014, 10, 1)) == 3

    def test_age_years_none(self):
        c = f.ChildFactory.build(birthdate=None)

        assert c.age_years(date(2014, 10, 1)) is None

    def test_age_display_under_one_month(self):
        c = f.ChildFactory.build(birthdate=date(2014, 9, 1))

        assert c.age_display(date(2014, 9, 10)) == "1wk"

    def test_age_display_under_two_years(self):
        c = f.ChildFactory.build(birthdate=date(2013, 9, 1))

        assert c.age_display(date(2014, 10, 1)) == "13mo"

    def test_age_display_over_two_years(self):
        c = f.ChildFactory.build(birthdate=date(2011, 9, 1))

        assert c.age_display(date(2014, 10, 1)) == "3yr"

    def test_age_display_none(self):
        c = f.ChildFactory.build(birthdate=None)

        assert c.age_display(date(2014, 10, 1)) == "?"


class TestSession:
    def test_str(self):
        assert str(f.SessionFactory.build(name="Bar")) == "Bar"

    def test_families(self, db, monkeypatch):
        monkeypatch.setattr(
            'wonderment.models.today', lambda: date(2014, 10, 1))
        s = f.SessionFactory.create(start_date=date(2014, 9, 12))
        p1 = f.ParticipantFactory.create(session=s, paid=30, parent__name="B")
        p2 = f.ParticipantFactory.create(session=s, paid=60, parent__name="A")
        f.ParticipantFactory.create(session=s, paid=0)
        f.ParticipantFactory.create(paid=30)
        s1a = f.ChildFactory.create(
            parent=p1.parent, birthdate=date(2008, 9, 20), name="1a")
        s1b = f.ChildFactory.create(
            parent=p1.parent, birthdate=date(2011, 10, 20), name="1b")
        s2a = f.ChildFactory.create(
            parent=p2.parent, birthdate=date(2010, 1, 20), name="2a")

        families = s.families()

        assert families['parents'] == [p2.parent, p1.parent]  # ordered by name
        assert list(families['students']) == [s1b, s2a, s1a]  # ordered by age
        assert [st.real_age for st in families['students']] == [
            "2yr", "4yr", "6yr"]

    def test_families_pretend_birthdate(self, db, monkeypatch):
        monkeypatch.setattr(
            'wonderment.models.today', lambda: date(2014, 9, 15))
        s = f.SessionFactory.create(start_date=date(2014, 9, 12))
        p = f.ParticipantFactory.create(session=s, paid=30)
        f.ChildFactory.create(
            parent=p.parent,
            birthdate=date(2011, 10, 1),
            pretend_birthdate=date(2011, 9, 1),
        )

        families = s.families()

        assert families['students'][0].real_age == "2yr"


class TestParticipant:
    def test_str(self):
        p = f.ParticipantFactory.build(
            parent__name="Parent", session__name="Session")

        assert str(p) == "Parent is signed up for Session"


denver = pytz.timezone('America/Denver')


class TestChildTransfer:
    def test_str(self):
        ct = f.ChildTransferFactory.build(
            child__name="Kid", in_out='in', initials='POK',
            timestamp=denver.localize(datetime(2017, 8, 18, 10))
        )

        assert str(ct) == "Kid signed in by POK at Fri Aug 18 10:00:00 2017"
