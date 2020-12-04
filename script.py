
import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_week_4.settings'
django.setup()

from vacancies import data
from vacancies.models import Company
from vacancies.models import Specialty
from vacancies.models import Vacancy


for specialty_data in data.specialties:
    specialty = Specialty.objects.create(
        code=specialty_data["code"],
        title=specialty_data['title'],
    )
    #specialty = Specialty.objects.all()

for company_data in data.companies:
    company = Company.objects.create(
        name=company_data['title'],
        location=company_data['location'],
        logo=company_data['logo'],
        description=company_data['description'],
        employee_count=company_data['employee_count'],
    )
     #company=Company.objects.all()

for vacancy_data in data.jobs:
    vacancy = Vacancy.objects.create(
        title=vacancy_data['title'],
        specialty=specialty,
        company=company,
        skills=vacancy_data['skills'],
        description=vacancy_data['description'],
        salary_min=vacancy_data['salary_from'],
        salary_max=vacancy_data['salary_to'],
        published_at=vacancy_data['posted']
    )
     #Vacancy.objects.all()
