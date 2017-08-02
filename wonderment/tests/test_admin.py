import datetime

from django.core.urlresolvers import reverse

from wonderment import queries
from wonderment.tests import factories as f


class TestParentAdmin(object):
    def test_new(self, app):
        admin = f.UserFactory.create(is_staff=True, is_superuser=True)
        session = f.SessionFactory.create(end_date=datetime.date.today())
        parent = f.ParentFactory.create()

        url = reverse('admin:wonderment_parent_changelist')

        resp = app.get(url, user=admin)

        assert queries.get_idhash_url(
            'edit_participant_form', parent, session=session) in resp.text
