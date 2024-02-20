from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path

from . import views

app_name = 'lab'

urlpatterns = [
    path('home',
         login_required(views.home),
         name='home'
         ),
    path('register-custom-user/',
         user_passes_test(lambda u: u.is_superuser)
         (login_required(views.register_custom_user)),
         name='register_custom_user'
         ),
    path('report-search/',
         login_required(views.report_search),
         name='report_search'
         ),
    path('send-img/',
         login_required(views.send_img),
         name='send_img'
         ),
    path('search-patient/',
         login_required(views.search_patient),
         name='search_patient'
         ),
    path('user/<int:user_id>/', login_required(views.patient_detail),
         name='patient_detail'
         ),
    path('edit-patient-data/<int:user_id>/',
         login_required(views.edit_patient_data),
         name='edit_patient_data'
         ),
    path('reports-profile/<int:user_id>/',
         login_required(views.reports_profile),
         name="reports_profile"
         ),
    path('report-detail/<int:report_id>/',
         login_required(views.report_detail),
         name="report_detail"
         ),
]
