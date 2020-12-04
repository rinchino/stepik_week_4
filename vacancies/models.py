from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User


class Specialty(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='images/pics/')
    pass

    def __str__(self):
        return self.title



class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='images/logo/')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pass

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=15)
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.CASCADE)
    skills = models.CharField(max_length=225)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=30)
    written_phone = PhoneField(blank=True, help_text='Contact phone number')
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, blank=True, null=True, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)





