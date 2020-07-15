from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from personal.models import Codal


def home(request):
    return render(request, 'home.html', {'name': 'ghazale'})


class AllCodalsView(View):
    def get(self, request):
        return render(
            request=request,
            template_name='codals.html',
            context={
                'codals': Codal.objects.all()
            }
        )
