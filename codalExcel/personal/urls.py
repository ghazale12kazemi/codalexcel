from django.urls import path

from personal.views import AllCodalsView

urlpatterns = [
    path('', AllCodalsView.as_view(), name='codals'),
]
