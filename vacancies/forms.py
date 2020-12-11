from django import forms

from vacancies.models import Vacancy, Company, Application


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('owner',)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': 'Ваше имя',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',

        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('company', 'published_at')
