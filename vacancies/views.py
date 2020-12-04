from django.core.checks import messages
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView

from vacancies.forms import ApplicationForm
from vacancies.models import Company
from vacancies.models import Specialty
# Create your views here.
from vacancies.models import Vacancy


class MainView(TemplateView):
    model = Company
    model = Vacancy
    model = Specialty
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data()
        context['companies'] = Company.objects.all()
        context['specialties'] = Specialty.objects.all()
        context['vacancies'] = Vacancy.objects.all()
        return context


class VacancyView(TemplateView):
    model = Vacancy
    model = Company
    template_name = 'vacancies_.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data()
        context['companies'] = Company.objects.all()
        context['vacancies'] = Vacancy.objects.all()
        return context


class VacancyCatView(TemplateView):
    model = Vacancy
    model = Specialty
    template_name = 'vacancy_cat.html'

    def get_context_data(self, specialty_code, **kwargs):
        context = super().get_context_data()
        specialty = get_object_or_404(Specialty, code=specialty_code)
        context['vacancies'] = Vacancy.objects.filter(specialty=specialty).select_related('company', 'specialty')
        context['title'] = specialty.title
        return context


class DetailVacancyView(TemplateView):
    model = Vacancy
    model = Company
    template_name = 'vacancy.html'

    def get_context_data(self, vacancy_id, **kwargs):
        context = super().get_context_data()
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        context['vacancy'] = vacancy
        context['application_form'] = ApplicationForm()
        return context

    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        application_form = self.form_class(request.Post)

        if not application_form.is_valid():
            return render(request, self.template_name, {
                'vacancy': vacancy,
                'application_form': application_form
            })
        if not request.user.is_authenticated:
            messages.error(request, 'Отклик могут оставить только авторизованные.')
            return render(request, self.template_name, {
                'vacancy': vacancy,
                'application_form': application_form,
            })

            application = application_form.save(commit=False)
            application.vacancy_id = vacancy_id
            application.user = request.user
            application.save()
            messages.info(request, 'Ваш отклик отправлен')
            return redirect(request.path)


class CompanyView(TemplateView):
    model = Vacancy
    model = Company
    template_name = 'company.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data()
        company = get_object_or_404(Company, id=id)
        context['vacancies'] = Vacancy.objects.filter(company=company).select_related('company', 'specialty')
        return context


def custom_handler500(request):
    return HttpResponseServerError('Внутреняя ошибка сервера')
