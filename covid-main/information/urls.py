"""covid19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="covid-homepage"),
    path('supplier_home.html', views.s_loginpage, name="supplier_homepage"),
    path('patient_register', views.patient_register, name="patient_register"),
    path('patient_login_homepage', views.patient_login, name="patient_login_homepage"),
    # path('edit_supplierprofile', views.edit_supplier_profile, name="edit_supplierprofile"),
    path('update_supplier', views.update_supplier, name="update_supplier"),
    path('profile_patient',views.profile_patient, name="profile_patient"),
    path('update_patient', views.update_patient, name="update_patient"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('book_now', views.book_now, name="book_now"),
    # path('health_care',views.health_care, name="health_care")
    path('book', views.book, name="book"),
    path('supplier_register', views.supplier_register, name="supplier_register")
]

