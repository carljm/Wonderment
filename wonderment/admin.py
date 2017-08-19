from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from . import (
    models,
    queries,
)


class ParticipantInline(admin.TabularInline):
    model = models.Participant
    extra = 0


class ChildInline(admin.TabularInline):
    model = models.Child
    extra = 0


class ClassInline(admin.TabularInline):
    model = models.Class
    extra = 0


class StudentInline(admin.TabularInline):
    model = models.Student
    extra = 0


class SessionQuestionInline(admin.TabularInline):
    model = models.SessionQuestion
    extra = 0


class SessionQuestionAnswerInline(admin.TabularInline):
    model = models.SessionQuestionAnswer
    extra = 0


class CommitteeMembershipInline(admin.TabularInline):
    model = models.Session.committee_members.through
    extra = 0
    verbose_name = "committee member"
    verbose_name_plural = "committee members"


class ParentAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'phone',
        'email',
        'registration_link',
    ]
    inlines = [ChildInline, ParticipantInline, SessionQuestionAnswerInline]

    def registration_link(self, obj):
        session = queries.get_next_upcoming_session()
        if session is None:
            return 'No upcoming session.'
        url = settings.BASE_URL + queries.get_idhash_url(
            'edit_participant_form', obj, session=session)
        return mark_safe('<a href="%s">%s</a>' % (url, url))


class TeacherAdmin(admin.ModelAdmin):
    inlines = [ClassInline]


class SessionQuestionAdmin(admin.ModelAdmin):
    inlines = [SessionQuestionAnswerInline]


class SessionAdmin(admin.ModelAdmin):
    inlines = [
        ParticipantInline,
        ClassInline,
        SessionQuestionInline,
        CommitteeMembershipInline,
    ]
    exclude = ['committee_members']


class ClassAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'session',
        'weekday',
        'start',
        'end',
        'min_age',
        'max_age',
        'max_students',
    ]
    list_filter = ['session']
    inlines = [StudentInline]


class ChildAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


admin.site.register(models.Parent, ParentAdmin)
admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.ClassDay)
admin.site.register(models.Class, ClassAdmin)
admin.site.register(models.Child, ChildAdmin)
admin.site.register(models.ParentArchive)
admin.site.register(models.ParticipantArchive)
admin.site.register(models.SessionQuestion, SessionQuestionAdmin)
