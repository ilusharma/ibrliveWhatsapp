from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    list_display = ('name','number','date')
    search_fields = ('name','number')


@admin.register(ContactGroup)
class ContactGroupAdmin(ImportExportModelAdmin):
    list_display = ('name','date')
    filter_horizontal = ('contacts',)

@admin.register(TemplateList)
class TemplateListAdmin(ImportExportModelAdmin):
    list_display = ('name','template','type','date')
    search_fields = ('name','template')

@admin.register(TemplateReport)
class TemplateReportAdmin(ImportExportModelAdmin):
    list_display = ('template','contact','date','seen','sent','seenTime','delivered')
    list_filter = ('template','contact','date','seen','sent','seenTime','delivered')
    search_fields = ('template','contact')

@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ('name','msg','date','contact')
    search_fields = ('name','msg','contact')
