from django.urls import path

from personal.views import AllCodalsView, RecentSymbolCodalsView

app_name = 'personal'

urlpatterns = [
    path('', AllCodalsView.as_view(), name='codals'),
    path('symbol-codals/', RecentSymbolCodalsView.as_view(), name='symbol_codals'),
]
