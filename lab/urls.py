from django.contrib.auth.decorators import user_passes_test
from django.urls import path

from . import views

app_name = 'lab'

urlpatterns = [
    path('home/',
         views.home,
         name='home'
         ),
    path('about/',
         views.about,
         name='about'
         ),
    path('register-custom-user/',
         user_passes_test(lambda u: u.is_superuser)
         (views.register_custom_user),
         name='register_custom_user'
         ),
    path('report-search/',
         views.report_search,
         name='report_search'
         ),
    path('send-img/',
         views.send_img,
         name='send_img'
         ),
    path('search-patient/',
         views.search_patient,
         name='search_patient'
         ),
    path('patient/<int:user_id>/',
         views.patient_detail,
         name='patient_detail'
         ),
    path('edit-patient-data/<int:user_id>/',
         views.edit_patient_data,
         name='edit_patient_data'
         ),
    path('reports-profile/<int:user_id>/',
         views.reports_profile,
         name="reports_profile"
         ),
    path('report-detail/<int:report_id>/',
         views.report_detail,
         name="report_detail"
         ),
]
