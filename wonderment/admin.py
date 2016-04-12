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


class StudentInline(admin.TabularInline):
    model = models.Student
    extra = 0


class ParentAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'phone',
        'email',
        'registration_link',
        'classes_link',
        'spring2016eval_link',
    ]
    inlines = [ParticipantInline, ChildInline]

    def registration_link(self, obj):
        url = settings.BASE_URL + obj.participant_url
        return mark_safe('<a href="%s">%s</a>' % (url, url))

    def classes_link(self, obj):
        url = settings.BASE_URL + obj.select_classes_url
        return mark_safe('<a href="%s">%s</a>' % (url, url))

    def spring2016eval_link(self, obj):
        url = settings.BASE_URL + obj.spring2016eval_url
        return mark_safe('<a href="%s">%s</a>' % (url, url))


class TeacherAdmin(admin.ModelAdmin):
    inlines = [ClassInline]


class SessionAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline, ClassInline]


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


class ClassDayAdmin(admin.ModelAdmin):
    inlines = [ChildAttendanceInline, ParentAttendanceInline]


admin.site.register(models.Parent, ParentAdmin)
admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.ClassDay, ClassDayAdmin)
admin.site.register(models.Class, ClassAdmin)
admin.site.register(models.Child, ChildAdmin)
admin.site.register(models.Chunk)
