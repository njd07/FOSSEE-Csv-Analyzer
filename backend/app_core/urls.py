from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('chart-data/', views.ChartDataView.as_view(), name='chart-data'),
    path('report/', views.ReportView.as_view(), name='report'),
    path('auth/token/', obtain_auth_token, name='api-token'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
]
