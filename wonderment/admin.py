from django.contrib import admin

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
    inlines = [ParticipantInline, ChildInline]


class SessionAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]


class ClassDayAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]


admin.site.register(models.Parent, ParentAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.ClassDay, ClassDayAdmin)
