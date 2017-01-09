from django.core.urlresolvers import reverse

from wonderment import queries
from wonderment.tests import factories as f


class TestParentAdmin(object):
    def test_new(self, app):
        admin = f.UserFactory.create(is_staff=True, is_superuser=True)
        parent = f.ParentFactory.create()

        url = reverse('admin:wonderment_parent_changelist')

        resp = app.get(url, user=admin)

        assert queries.get_idhash_url('fall2016eval', parent) in resp.text
