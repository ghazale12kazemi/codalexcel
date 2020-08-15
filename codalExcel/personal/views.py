from django.shortcuts import render, get_object_or_404
from django.views import View

from personal.models import Codal, Symbol
from .filters import OrderFilter


class AllCodalsView(View):
    def get(self, request):
        codals = Codal.objects.all()

        myFilter = OrderFilter(request.GET, queryset=codals)
        codals = myFilter.qs

        context = {'codals': codals, 'myFilter': myFilter}

        return render(
            request=request,
            template_name='codals.html',
            context=context
        )


class RecentSymbolCodalsView(View):
    def get(self, request, symbol_slug):
        sym = get_object_or_404(Symbol, slug=symbol_slug)
        codals = sym.codal_set.all()

        try:
            c3 = codals.filter(type='miyandore', duration__in=['3', '۳']).last()
        except Codal.DoesNotExist:
            c3 = None

        try:
            c6 = codals.filter(type='miyandore', duration__in=['6', '۶']).last()
        except Codal.DoesNotExist:
            c6 = None

        try:
            c9 = codals.filter(type='miyandore', duration__in=['9', '۹']).last()
        except Codal.DoesNotExist:
            c9 = None

        try:
            c12 = codals.filter(type='salane', duration__in=['12', '۱۲']).last()
        except Codal.DoesNotExist:
            c12 = None

        return render(
            request=request,
            template_name='symbol_codals.html',
            context={
                'symbol': sym,
                'c3': c3,
                'c6': c6,
                'c9': c9,
                'c12': c12,
            }
        )
