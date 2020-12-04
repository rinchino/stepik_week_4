from django.contrib import admin

# Register your models here.
from vacancies.models import Specialty, Company

class VacancyAdmin(admin.ModelAdmin):
    fields = ['logo', 'picture']


admin.site.register(Company)
admin.site.register(Specialty)
