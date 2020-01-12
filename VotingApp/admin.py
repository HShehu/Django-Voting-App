from django.contrib import admin
from .models import Poll,Choice,Contestant



admin.site.site_header = "447 Admin"
admin.site.site_title = "447 Admin Area"
admin.site.index_title = "Welcome To 447 Admin Area"

# Register your models here.
class ChoiceInLine(admin.TabularInline):
    model = Choice
    readonly_fields = ('votes',)
    extra = 0


class PollAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['poll_text']}),
    ('Date Information', {'fields': ['start_date','end_date'], 'classes': ['collapse']}),]
    inlines = [ChoiceInLine]

class ContestantAdmin(admin.ModelAdmin):
    list_display = ('user','poll','approved',)
    ordering = ('approved',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Contestant, ContestantAdmin)

