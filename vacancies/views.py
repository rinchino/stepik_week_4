from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import TemplateView, TemplateResponseMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from vacancies.forms import ApplicationForm, CompanyForm, VacancyForm
from vacancies.models import Company
from vacancies.models import Specialty
# Create your views here.
from vacancies.models import Vacancy, Application


class MySignupView(CreateView):
   form_class = UserCreationForm
   success_url = 'login'
   template_name = 'register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


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
    model=Vacancy
    model=Company
    model=Application
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
            return redirect(request.path)


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

        company=company_form.save(commit=False)
        if company.owner is None:
            company.owner=request.user
        company.save()
        messages.info(request, 'Информация о компании обновлена')
        return redirect(request.path)


class MyCompanyVacancies(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name='company/vacancy-list.html'

    def get(self, request, **kwargs):
        try:
            return self.render_to_response({
                'vacancies': Vacancy.objects.filter(company=self.request.user.company),
            })
        except ObjectDoesNotExist:
            raise Http404(f'User"{self.request.user.username}" have no company')


class MycompanyVacancy(LoginRequiredMixin, FormMixin, DetailView):
   model = Vacancy
   context_object_name = 'vacancy'
   form_class = VacancyForm
   template_name = 'company/vacancy-edit.html'
   pk_url_kwarg = 'vacancy_id'
   queryset = Vacancy.objects.select_related('company', 'specialty')
   def get_context_data(self, **kwargs):
       context = super().get_context_data()
       return context


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
