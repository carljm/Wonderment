from django.core.urlresolvers import reverse

from wonderment import (
    models,
    queries,
)
from wonderment.tests import factories as f


class TestParticipantForm:
    def test_new(self, app, monkeypatch):
        monkeypatch.setattr('wonderment.forms.ChildFormSet.extra', 1)

        session = f.SessionFactory.create()

        url = reverse(
            'new_participant_form',
            kwargs={'session_id': session.id},
        )
        form = app.get(url).forms['participant-form']
        form['name'] = "someone"
        form['email'] = 'someone@example.com'
        form['phone'] = '321-6543-9876'
        form['children-0-name'] = "Kid"
        form.submit().follow()

        participant = models.Participant.objects.get()
        parent = participant.parent
        child = parent.children.get()
        assert parent.name == "someone"
        assert parent.email == 'someone@example.com'
        assert parent.phone == '321-6543-9876'
        assert child.name == "Kid"
        assert participant.session == session

    def test_edit(self, app, monkeypatch):
        monkeypatch.setattr('wonderment.forms.ChildFormSet.extra', 1)

        session = f.SessionFactory.create()
        participant = f.ParticipantFactory.create(
            session=session,
            parent__name='old',
            parent__email='old@example.com',
            parent__phone='321-654-9876',
        )
        parent = participant.parent
        f.ChildFactory.create(parent=parent, name='old')
        f.ChildFactory.create(parent=parent, name='old')

        form_url = queries.get_idhash_url(
            'edit_participant_form', parent, session)

        form = app.get(form_url).forms['participant-form']
        form['name'] = "someone"
        form['children-0-name'] = "Kid"
        form['children-1-DELETE'] = True
        form['children-2-name'] = "Hey"
        form.submit().follow()

        participant = models.Participant.objects.get()
        parent = participant.parent
        child_names = {c.name for c in parent.children.all()}
        assert parent.name == "someone"
        assert child_names == {"Kid", "Hey"}


class TestClassAttendance:
    def test_loads(self, app):
        assistant = f.UserFactory.create()
        session = f.SessionFactory.create()
        participant = f.ParticipantFactory.create(session=session)
        klass = f.ClassFactory.create(session=session)
        student = f.StudentFactory.create(klass=klass, child__name="Kid One")
        student = f.StudentFactory.create(klass=klass, child__name="Kid Two")

        url = reverse(
            'class_attendance',
            kwargs=dict(session_id=session.id, class_id=klass.id),
        )
        resp = app.get(url, user=assistant)

        resp.mustcontain("Kid One", "Kid Two")


class TestSignInOut:
    def test_loads(self, app):
        assistant=f.UserFactory.create()
        student = f.StudentFactory.create(
            child__name="Kid One",
            child__parent__name="The Parent",
            child__parent__pick_up_names="Pick Up Person",
        )

        url = reverse(
            'sign_in_out',
            kwargs={
                'session_id': student.klass.session_id,
                'class_id': student.klass_id,
                'child_id': student.child_id,
            },
        )

        resp = app.get(url, user=assistant)

        resp.mustcontain("Kid One", "The Parent", "Pick Up Person")
