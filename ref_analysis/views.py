from django.shortcuts import render
from .models import ResultsJ1

def match_list(request):
    matches = ResultsJ1.objects.all()
    return render(request, 'ref_analysis/match_list.html', {'matches':matches})