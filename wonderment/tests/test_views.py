from django.core.urlresolvers import reverse

from wonderment import models, views
from wonderment.tests import factories as f


class TestParticipantForm(object):
    def test_new(self, app, monkeypatch):
        monkeypatch.setattr('wonderment.forms.ChildFormSet.extra', 1)

        url = reverse('new_participant_form')
        form = app.get(url).forms['participant-form']
        form['name'] = "someone"
        form['level'] = 'weekly'
        form['payment'] = 'early'
        form['children-0-name'] = "Kid"
        resp = form.submit().follow()

        resp.mustcontain("http://wondermentblackhills.com/register/")
        participant = models.Participant.objects.get()
        parent = participant.parent
        child = parent.children.get()
        assert participant.level == 'weekly'
        assert participant.payment == 'early'
        assert parent.name == "someone"
        assert child.name == "Kid"
        assert participant.session.name == views.CURRENT_SESSION_NAME

    def test_edit(self, app, monkeypatch):
        monkeypatch.setattr('wonderment.forms.ChildFormSet.extra', 1)

        session = views.current_session()
        participant = f.ParticipantFactory.create(
            session=session,
            level='monthly',
            payment='later',
            parent__name='old',
        )
        parent = participant.parent
        f.ChildFactory.create(parent=parent, name='old')
        f.ChildFactory.create(parent=parent, name='old')

        form = app.get(parent.participant_url).forms['participant-form']
        form['name'] = "someone"
        form['level'] = 'weekly'
        form['payment'] = 'early'
        form['children-0-name'] = "Kid"
        form['children-1-DELETE'] = True
        form['children-2-name'] = "Hey"
        resp = form.submit().follow()

        resp.mustcontain("http://wondermentblackhills.com/register/")
        participant = models.Participant.objects.get()
        parent = participant.parent
        child_names = {c.name for c in parent.children.all()}
        assert participant.level == 'weekly'
        assert participant.payment == 'early'
        assert parent.name == "someone"
        assert child_names == {"Kid", "Hey"}
