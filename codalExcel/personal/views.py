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
    def get(self, request):
        NOT_FOUND = ''
        sales = []
        symbols = []
        for sym in Symbol.objects.all():
            symbols.append(sym.slug)
            codal_set = sym.codal_set.filter(type__in=['salane', 'talfigi', 'miyandore']) \
                .annotate(int_duration=RawSQL('CAST(duration AS UNSIGNED)', params=[])) \
                .annotate(int_years=RawSQL('CAST(years AS UNSIGNED)', params=[]))
            sym_sales = []
            for year in range(1398, 1400):
                year_codals = codal_set.filter(int_years=year)
                prev_codal = None
                for duration in (3, 6, 9, 12):
                    codals = year_codals.filter(int_duration=duration).all()
                    success = False
                    for cur_codal in codals:
                        if success:
                            break
                        try:
                            if prev_codal is None:
                                sym_sales.append(int(cur_codal.forosh))
                            else:
                                sym_sales.append(int(cur_codal.forosh) - int(prev_codal.forosh))
                            success = True
                            prev_codal = cur_codal
                        except Exception as e:
                            pass
                    if len(codals) == 0:
                        sym_sales.append(NOT_FOUND)
                    elif not success:
                        sym_sales.append('BAD')
            sales.append(sym_sales)

        dates = []
        for year in range(1398, 1400):
            for duration in (3, 6, 9, 12):
                dates.append('{}/{}'.format(year, duration))
        
        while not any(filter(lambda sale: sale[0] != NOT_FOUND, sales)):
            sales = list(map(lambda sale: sale[1:], sales))
            dates = dates[1:]
        
        while not any(filter(lambda sale: sale[-1] != NOT_FOUND, sales)):
            sales = list(map(lambda sale: sale[:-1], sales))
            dates = dates[0:-1]

        sales = list(sales)
        for i, sym in enumerate(symbols):
            sales[i].insert(0, sym)

        return render(
            request=request,
            template_name='symbol_codals.html',
            context={
                'thead': dates,
                'tbody': sales,
            }
        )

