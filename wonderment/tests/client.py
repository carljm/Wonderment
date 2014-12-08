"""
Webapp integration test client.

"""
import django_webtest


class TestClient(django_webtest.DjangoTestApp):
    """A WebTest-based test client for webapp integration tests."""
    xhr_default = False

    def get(self, *a, **kw):
        return super(TestClient, self).get(*a, **self._update_kw(kw))

    def post(self, *a, **kw):
        return super(TestClient, self).post(*a, **self._update_kw(kw))

    def put(self, *a, **kw):
        return super(TestClient, self).put(*a, **self._update_kw(kw))

    def patch(self, *a, **kw):
        return super(TestClient, self).patch(*a, **self._update_kw(kw))

    def delete(self, *a, **kw):
        return super(TestClient, self).delete(*a, **self._update_kw(kw))

    def options(self, *a, **kw):
        return super(TestClient, self).options(*a, **self._update_kw(kw))

    def head(self, *a, **kw):
        return super(TestClient, self).head(*a, **self._update_kw(kw))

    def post_json(self, *a, **kw):
        return super(TestClient, self).post_json(*a, **self._update_kw(kw))

    def put_json(self, *a, **kw):
        return super(TestClient, self).put_json(*a, **self._update_kw(kw))

    def patch_json(self, *a, **kw):
        return super(TestClient, self).patch_json(*a, **self._update_kw(kw))

    def delete_json(self, *a, **kw):
        return super(TestClient, self).delete_json(*a, **self._update_kw(kw))

    def _update_kw(self, kw):
        kw['extra_environ'] = self._update_environ(
            kw.get('extra_environ'), kw.pop('user', None))
        if kw.pop('xhr', self.xhr_default):
            kw.setdefault('headers', {}).setdefault(
                'X-Requested-With', 'XMLHttpRequest')
        return kw
