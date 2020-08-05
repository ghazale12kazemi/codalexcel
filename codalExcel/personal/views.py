from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from personal.models import Codal

from .filters import OrderFilter


class AllCodalsView(View):
    def get(self, request):

        codals = Codal.objects.all()

        myFilter = OrderFilter(request.GET, queryset= codals)
        codals = myFilter.qs

        context = {'codals': codals,'myFilter':myFilter }


        return render(
            request=request,
            template_name='codals.html',
            context = context
        )
