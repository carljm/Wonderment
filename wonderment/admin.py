from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class ParticipantInline(admin.TabularInline):
    model = models.Participant
    extra = 0


class ChildInline(admin.TabularInline):
    model = models.Child
    extra = 0


class ChildAttendanceInline(admin.TabularInline):
    model = models.ChildAttendance
    extra = 0


class ParentAttendanceInline(admin.TabularInline):
    model = models.ParentAttendance
    extra = 0


class ClassInline(admin.TabularInline):
    model = models.Class
    extra = 0


class ParentAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'phone',
        'email',
        'registration_link',
        'fall2015eval_link',
    ]
    inlines = [ParticipantInline, ChildInline]

    def registration_link(self, obj):
        url = settings.BASE_URL + obj.participant_url
        return mark_safe('<a href="%s">%s</a>' % (url, url))

    def fall2015eval_link(self, obj):
        url = settings.BASE_URL + obj.fall2015eval_url
        return mark_safe('<a href="%s">%s</a>' % (url, url))


class TeacherAdmin(admin.ModelAdmin):
    inlines = [ClassInline]


class SessionAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline, ClassInline]


class ClassDayAdmin(admin.ModelAdmin):
    inlines = [ChildAttendanceInline, ParentAttendanceInline]


admin.site.register(models.Parent, ParentAdmin)
admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.ClassDay, ClassDayAdmin)
