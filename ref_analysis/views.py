from django.shortcuts import render
from .models import ResultsJ1
from .models import Teams
from .models import Referees


def search_form(request):
    # 検索フォーム内の情報を取得
    teams = Teams.objects.all # j1チーム
    referees = Referees.objects.all() # 主審

    content = {'teams':teams, 'referees':referees}

    return render(request, 'ref_analysis/search_form.html', content)

def search_result(request):
    # 検索条件を取得
    team_id = request.GET.get('team_id')
    referee_id = request.GET.get('referee_id')
    term = request.GET.get('term')


    matches = ResultsJ1.objects.filter(
        home_team_id=team_id
    )


    return render(request, 'ref_analysis/result.html', {'matches': matches})

def match_list(request):
    matches = ResultsJ1.objects.all()
    return render(request, 'ref_analysis/match_list.html', {'matches':matches})