from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Profile, Candidates

admin.site.register(Profile)


@admin.register(Candidates)
class ViewAdmin(ImportExportModelAdmin):
    exclude = ('id',)
