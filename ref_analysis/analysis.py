def calculate_stats(matches, team_id):
    # 試合データを新しい順にソート
    ordered_matches = matches.order_by('-match_date')
    
    # 戦績を算出
    win_count = 0
    lose_count = 0
    draw_count = 0
    goals_for = 0
    goals_against = 0

    for match in ordered_matches:
        # 検索対象チームと対戦相手の得点数を算出
        if match.home_team_id == team_id:
            target_team_goal = int(match.home_team_goal)
            opponent_team_goal = int(match.away_team_goal)
        elif match.away_team_id == team_id:
            target_team_goal = int(match.away_team_goal)
            opponent_team_goal = int(match.home_team_goal)
        else:
            continue

        goals_for += target_team_goal
        goals_against += opponent_team_goal

        # 勝敗分数を算出
        if target_team_goal > opponent_team_goal:
            win_count += 1
        elif target_team_goal < opponent_team_goal:
            lose_count += 1
        else:
            draw_count += 1

    # 試合数
    match_count = win_count + lose_count + draw_count

    # 平均成績
    win_rate = win_count / match_count * 100
    avg_goals_for = goals_for / match_count
    avg_goals_against = goals_against / match_count

    # 直近5試合データ
    recent_five_matches = ordered_matches[:5]

    return {
        "games": match_count,
        "wins": win_count,
        "draws": draw_count,
        "loses": lose_count,
        "win_rate": win_rate,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "avg_goals_for": avg_goals_for,
        "avg_goals_against": avg_goals_against,
        "recent_matches": recent_five_matches,
    }