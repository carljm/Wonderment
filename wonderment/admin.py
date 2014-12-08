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


class AttendanceInline(admin.TabularInline):
    model = models.Attendance
    extra = 0


class ParentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'email', 'registration_link']
    inlines = [ParticipantInline, ChildInline]

    def registration_link(self, obj):
        url = settings.BASE_URL + obj.participant_url
        return mark_safe('<a href="%s">%s</a>' % (url, url))


class SessionAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]


class ClassDayAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]


admin.site.register(models.Parent, ParentAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.ClassDay, ClassDayAdmin)
