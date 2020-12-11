from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView, TemplateResponseMixin

from vacancies import models
from vacancies.forms import ApplicationForm, CompanyForm, VacancyForm
from vacancies.models import Company
from vacancies.models import Specialty
# Create your views here.
from vacancies.models import Vacancy


class MySignupView(CreateView):
    form_class=UserCreationForm
    success_url='/login'
    template_name='register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user=True
    template_name='login.html'


class MainView(TemplateView):
    model=Company
    model=Vacancy
    model=Specialty
    template_name='main.html'

    def get_context_data(self, **kwargs):
        context=super(MainView, self).get_context_data()
        context['companies']=Company.objects.all()
        context['specialties']=Specialty.objects.all()
        context['vacancies']=Vacancy.objects.all()
        return context


class VacancyView(TemplateView):
    model=Vacancy
    model=Company
    template_name='vacancies_.html'

    def get_context_data(self, **kwargs):
        context=super(VacancyView, self).get_context_data()
        context['companies']=Company.objects.all()
        context['vacancies']=Vacancy.objects.all()
        return context


class VacancyCatView(TemplateView):
    model=Vacancy
    model=Specialty
    template_name='vacancy_cat.html'

    def get_context_data(self, specialty_code, **kwargs):
        context=super().get_context_data()
        specialty=get_object_or_404(Specialty, code=specialty_code)
        context['vacancies']=Vacancy.objects.filter(specialty=specialty).select_related('company', 'specialty')
        context['title']=specialty.title
        return context


class DetailVacancyView(TemplateView):
    form_class=ApplicationForm
    template_name='vacancy.html'

    def get_context_data(self, vacancy_id, **kwargs):
        context=super().get_context_data()
        vacancy=get_object_or_404(Vacancy, pk=vacancy_id)
        context['vacancy']=vacancy
        context['application_form']=ApplicationForm()
        return context

    def post(self, request, vacancy_id):
        vacancy=get_object_or_404(Vacancy, pk=vacancy_id)
        application_form=self.form_class(request.POST)

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

        application=application_form.save(commit=False)
        application.vacancy_id=vacancy_id
        application.user=request.user
        application.save()
        messages.info(request, 'Ваш отклик отправлен')
        return render(request, 'sent.html')


@login_required
def mycompany_create(request):
    return render(request, 'company/company-create.html')


class MyCompanyView(LoginRequiredMixin, TemplateResponseMixin, View):
    form_class=CompanyForm
    template_name='company/company-edit.html'

    def get(self, request, *args, **kwargs):
        try:
            return self.render_to_response({
                'form': self.form_class(instance=request.user.company),
            })
        except ObjectDoesNotExist:
            return self.render_to_response({
                'form': self.form_class(),
            })

    def post(self, request):
        try:
            company_form=self.form_class(request.POST, request.FILES, instance=request.user.company)
        except ObjectDoesNotExist:
            company_form=self.form_class(request.POST, request.FILES)

        if not company_form.is_valid():
            return self.render_to_response({
                'form': company_form,
            })

        company=company_form.save(commit=True)
        if company.owner is None:
            company.owner=request.user
        company.save()
        messages.info(request, 'Информация о компании обновлена')
        return redirect(request.path)


class MyCompanyVacancies(View):
    def get(self, request, *args, **kwargs):
        company=Company.objects.filter(owner=request.user).first()
        vacancies=company.vacancies.annotate(count=Count('applications')) \
            .all()
        if len(vacancies) == 0:
            return render(
                request,
                'company/vacancy-list.html',
                context={
                    'title': 'У вас пока нет вакансий,'
                             ' но вы можете создать первую!',
                    'number_vacancies': len(vacancies),
                }
            )
        else:
            return render(
                request,
                'company/vacancy-list.html',
                context={
                    'companies': company,
                    'vacancies': vacancies,
                    'title': '',
                    'number_vacancies': len(vacancies),
                }
            )


class MyVacanciesСreateView(View):
    def get(self, request, *args, **kwargs):
        vacancy_form=VacancyForm()
        return render(
            request,
            'company/vacancy-edit.html',
            context={
                'title': 'Создайте карточку вакансии',
                'vacancy_form': vacancy_form,
            }
        )

    def post(self, request, *args, **kwargs):
        my_company_vac=models.Company.objects.filter(owner=request.user)
        vacancy_form=VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy=vacancy_form.save(commit=False)
            vacancy.company=my_company_vac.first()
            vacancy.save()
            return redirect(
                request.path,
                context={
                    'title': 'Вакансия создана'
                }
            )
        else:
            return render(
                request, 'vacancy-edit.html',
                context={
                    'title': 'Создайте вакансию',
                    'vacancy_form': vacancy_form
                }
            )


class MyVacancyEditView(View):
    def get(self, request, id, *args, **kwargs):
        vacancy=Vacancy.objects.filter(id=id).first()
        if not vacancy:
            raise Http404
        applications=vacancy.applications.all()
        return render(
            request,
            'company/vacancy-edit.html',
            context={
                'vacancy_form': VacancyForm(instance=vacancy),
                'title': 'Хотите отредактировать вакансию?',
                'applications': applications,
                'number_applications': len(applications),
            }
        )

    def post(self, request, id, *args, **kwargs):
        my_company_vac=models.Company.objects.filter(owner=request.user)
        vacancy=models.Vacancy.objects.filter(
            id=id, company=my_company_vac.first()) \
            .first()
        vacancy_form=VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy_form=VacancyForm(request.POST,
                                     request.FILES,
                                     instance=vacancy)
            vacancy_form.save()
            return HttpResponseRedirect(request.path, )
        else:
            return render(
                request, 'vacancy-edit.html',
                context={'title': 'Отредактируйте вакансию',
                         'vacancy_form': vacancy_form
                         }
            )


class CompanyView(TemplateView):
    model=Vacancy
    model=Company
    template_name='company.html'

    def get_context_data(self, id, **kwargs):
        context=super().get_context_data()
        company=get_object_or_404(Company, id=id)
        context['vacancies']=Vacancy.objects.filter(company=company).select_related('company', 'specialty')
        return context


def custom_handler500(request):
    return HttpResponseServerError('Внутреняя ошибка сервера')
