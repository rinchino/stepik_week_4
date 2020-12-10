"""stepik_week3 URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url

#from django.template.context_processors import static
from django.contrib.auth.views import LogoutView
from django.urls import include
from django.urls import path
from django.urls import path, include
#from stepik_week_4 import settings
from vacancies import views
from vacancies.views import CompanyView, MyCompanyView, MyCompanyVacancies, MyLoginView, MySignupView, \
    MyCompanyCreateView
from vacancies.views import DetailVacancyView
from vacancies.views import MainView
from vacancies.views import VacancyCatView
from vacancies.views import VacancyView




urlpatterns = [

    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacancyView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty_code>/', VacancyCatView.as_view(), name='vacancy_by_specialization'),
    path('vacancies/<int:vacancy_id>/', DetailVacancyView.as_view(), name='detail_vacancy'),
    path('vacancies/<vacancy_id>/send/', DetailVacancyView.as_view()),
    path('companies/<int:id>', CompanyView.as_view(), name='company'),
    path('mycompany/', views.MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/create', views.mycompany_create, name='mycompany_create'),
    path('mycompany/vacancies', views.MyCompanyVacancies.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/create', views.MyCompanyCreateView.as_view(), name='mycompany_vacancy_create'),
    path('mycompany/vacancies/<int:vacancy_id>', views.MycompanyVacancy.as_view(), name='mycompany_vacancy'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('login/', MyLoginView.as_view(), name='login'),
    url('logout/', LogoutView.as_view(), name='logout'),
    path('register/', MySignupView.as_view(), name='register'),
    #url(r'^account/', include('account.urls')),
    #url(r'^admin/', admin.site.urls),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
