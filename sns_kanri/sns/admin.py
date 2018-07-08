from django.contrib import admin

from sns_kanri.sns.models import SNS, Record


class SNSAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'sns', 'user', 'date', 'time', 'updated']
    list_filter = ['sns', 'user', 'date', 'time']


admin.site.register(SNS, SNSAdmin)
admin.site.register(Record, RecordAdmin)
