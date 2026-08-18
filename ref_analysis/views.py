from django.shortcuts import render
from .models import ResultsJ1
from .models import Teams
from .models import Referees
from django.db.models import Q
from datetime import date
from .analysis import calculate_stats


def search_form(request):
    # 検索フォーム内の情報を取得
    teams = Teams.objects.all # 全チーム
    referees = Referees.objects.all() # 主審

    content = {'teams':teams, 'referees':referees}

    return render(request, 'ref_analysis/search_form.html', content)

def search_result(request):

    # 検索条件を取得
    team_id = request.GET.get('team_id')
    referee_id = request.GET.get('referee_id')
    term = request.GET.get('term')

    # 検索条件の空チェック
    if any(value is None or value == '' for value in [team_id, referee_id, term]):
        raise ValueError('必要な項目が入力されていません')

    term = int(term) # 値検証後にint変換

    # DBからチーム名と審判名を取得
    team_name = Teams.objects.get(team_id=team_id).team_name
    referee_name = Referees.objects.get(referee_id=referee_id).referee_name
    

    #検索期間の算出
    year = date.today().year - 1
    seasons = [year - i for i in range(term)]
    season_from = seasons[-1]
    season_to = seasons[0]

    #対象チームのホーム&アウェイの試合を検索期間分のみ取得
    matches = ResultsJ1.objects.filter(season__in=seasons).filter(Q(home_team_id=team_id) | Q(away_team_id=team_id)).filter(referee_id=referee_id)

    # 検索結果が0件の場合
    if matches.count() == 0:
        return render(request, 'ref_analysis/no_result.html', {'team_name': team_name, 'referee_name': referee_name, 'season_from': season_from, 'season_to': season_to})

    # 取得した試合結果から戦績を算出
    stats = calculate_stats(matches, team_id)


    return render(request, 'ref_analysis/result.html', {'stats': stats, 'team_id': team_id, 'team_name': team_name, 'referee_name': referee_name, 'season_from': season_from, 'season_to': season_to})


# 検索画面へ戻るボタン押下時
def back_to_search_form(request):
    search_form()

def match_list(request):
    matches = ResultsJ1.objects.all()
    return render(request, 'ref_analysis/match_list.html', {'matches':matches})