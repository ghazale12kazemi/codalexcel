from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models.expressions import RawSQL

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
        codals = sym.codal_set.filter(type__in=['talfigi']).all()
        if codals:
            codals = sym.codal_set.filter(type__in=['talfigi','miyandore']) \
                .annotate(int_duration=RawSQL('CAST(duration AS UNSIGNED)', params=[])) \
                .annotate(int_years=RawSQL('CAST(years AS UNSIGNED)', params=[])) \
                .order_by('int_years','int_duration').all()
        else:
            codals = sym.codal_set.filter(type__in=['salane', 'miyandore']) \
                .annotate(int_duration=RawSQL('CAST(duration AS UNSIGNED)', params=[])) \
                .annotate(int_years=RawSQL('CAST(years AS UNSIGNED)', params=[])) \
                .order_by('int_years', 'int_duration').all()
        sell_volume = []
        report_date = []
        frosh_list = []
        previous_codal = None

        print([(codal.id, codal.years, codal.int_duration) for codal in codals])


        for codal in codals:
            if codal.duration == '3' or previous_codal is None:
                sell_volume.append(int(codal.forosh))
            else:
                sell_volume.append(int(codal.forosh) - int(previous_codal.forosh))
            report_date.append('{}/{}'.format(codal.int_years, codal.int_duration))
            frosh_list.append(codal.forosh)
            previous_codal = codal


        return render(
            request=request,
            template_name='symbol_codals.html',
            context={
                'symbol': sym,
                'sell_list': sell_volume,
                'date_list': report_date,
                'frosh_list':frosh_list,
            }
        )

