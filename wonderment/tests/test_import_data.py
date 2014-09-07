import csv
import datetime
import os
import tempfile

from wonderment.import_data import import_csv, FIELDS
from wonderment import models
from wonderment.tests import factories as f


def do(*rows, **kwargs):
    """Create temp CSV file from given row dicts and import it.

    Given field names should be short versions, will be translated.

    Order of fields is not guaranteed.

    """
    if 'session' in kwargs:
        session = kwargs['session']
    else:
        session = f.SessionFactory.create()
    tf = tempfile.NamedTemporaryFile(
        prefix='wonderment-tests-tmp-', mode='w', newline='', delete=False)
    try:
        writer = csv.DictWriter(tf.file, FIELDS.values())
        writer.writeheader()
        for row in rows:
            row.setdefault('level', 'ALL fall classes')
            translated = {FIELDS[k]: v for k, v in row.items()}
            writer.writerow(translated)
        tf.close()
        import_csv(session, tf.name)
    finally:
        os.remove(tf.name)


class TestImportCsv(object):
    def test_parent_info(self, db):
        do({
            'first': "First",
            'last': "Last",
            'address': "123 N Main",
            'phone': '321-654-0987',
            'phone_type': 'cell',
            'email': 'foo@example.com',
            'preferred': 'email',
            'age_groups': "Any",
            'could_teach': "Whatev",
            'could_assist': "Anywhere",
            'all_ages_help': "Yes!",
            'other_contributions': "Everything",
            'classes_desired': "All",
            'spouse': "Spouse",
            'spouse_contact': "spouse contact",
            'emergency': "Emergency",
            'emergency_contact': "emergency contact",
        })

        p = models.Parent.objects.get()
        assert p.name == "First Last"
        assert p.address == "123 N Main"
        assert p.phone == '321-654-0987'
        assert p.phone_type == 'cell'
        assert p.email == 'foo@example.com'
        assert p.preferred == 'email'
        assert p.age_groups == "Any"
        assert p.could_teach == "Whatev"
        assert p.could_assist == "Anywhere"
        assert p.all_ages_help == "Yes!"
        assert p.other_contributions == "Everything"
        assert p.classes_desired == "All"
        assert p.spouse == "Spouse"
        assert p.spouse_contact == "spouse contact"
        assert p.emergency == "Emergency"
        assert p.emergency_contact == "emergency contact"

    def test_clean_phone_type(self, db):
        do(
            {'phone_type': 'mobile'},
            {'phone_type': 'Cell'},
            {'phone_type': 'cellular'},
            {'phone_type': '605-123-4567'},
        )

        types = models.Parent.objects.values_list('phone_type', flat=True)

        assert sorted(types) == ['', 'cell', 'cell', 'cell']

    def test_clean_preferred(self, db):
        do(
            {'preferred': 'foo'},
        )

        types = models.Parent.objects.values_list('preferred', flat=True)

        assert sorted(types) == ['']

    def test_participation(self, db):
        session = f.SessionFactory.create()

        do(
            {
                'paid': 100,
                'level': 'ALL fall classes',
            },
            {
                'paid': 50,
                'level': 'Monthly all ages gatherings ONLY',
            },
            session=session,
        )

        for parent in models.Parent.objects.all():
            p = parent.participations.get()
            assert p.session == session
            assert p.paid in {50, 100}
            assert p.level == 'monthly' if p.paid == 50 else 'weekly'

    def test_children(self, db):
        do(
            {
                'name1': "First Kid",
                'gender1': 'girl',
                'special1': "Special",
                'bday1': '11/7/2009',
            },
        )

        child = models.Parent.objects.get().children.get()
        assert child.name == "First Kid"
        assert child.gender == 'female'
        assert child.special_needs == "Special"
        assert child.birthdate == datetime.date(2009, 11, 7)