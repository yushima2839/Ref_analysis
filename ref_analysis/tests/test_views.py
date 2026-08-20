from django.test import TestCase
from ref_analysis.models import Teams, Referees, ResultsJ1
from unittest.mock import patch

class SearchFormViewTestCase(TestCase):

    # テストデータのセットアップ
    def setUp(self):
        # チーム
        self.team = Teams.objects.create(team_id='t001', team_name='鹿島アントラーズ', team_category='1')  
        # 主審
        self.referee1 = Referees.objects.create(referee_id='r001', referee_name='木村 博之')
        self.referee2 = Referees.objects.create(referee_id='r002', referee_name='池内 明彦')
        # 試合
        # 2025シーズン
        self.match_2025 =  ResultsJ1.objects.create(
            match_id='m001',
            match_date='2025-08-01',
            home_team_id='t001',
            home_team='鹿島アントラーズ',
            away_team_id='t002',
            away_team='ガンバ大阪',
            home_team_goal=2,
            away_team_goal=1,
            referee='木村 博之',
            referee_id='r001',
            season='2025',
            category='1',
            winner_team_id='t001'
        )
        # 2024シーズン
        self.match_2024 = ResultsJ1.objects.create(
            match_id='m002',
            match_date='2024-08-01',
            home_team_id='t001',
            home_team='鹿島アントラーズ',
            away_team_id='t002',
            away_team='ガンバ大阪',
            home_team_goal=1,
            away_team_goal=1,
            referee='木村 博之',
            referee_id='r001',
            season='2024',
            category='1',
            winner_team_id=''
        )
        # 2023シーズン
        self.match_2023 = ResultsJ1.objects.create(
            match_id='m003',
            match_date='2023-08-01',
            home_team_id='t002',
            home_team='ガンバ大阪',
            away_team_id='t001',
            away_team='鹿島アントラーズ',
            home_team_goal=0,
            away_team_goal=2,
            referee='木村 博之',
            referee_id='r001',
            season='2023',
            category='1',
            winner_team_id='t001'
        )
        # 2023シーズン
        self.match_2022 = ResultsJ1.objects.create(
            match_id='m004',
            match_date='2022-08-01',
            home_team_id='t002',
            home_team='ガンバ大阪',
            away_team_id='t001',
            away_team='鹿島アントラーズ',
            home_team_goal=0,
            away_team_goal=2,
            referee='木村 博之',
            referee_id='r001',
            season='2022',
            category='1',
            winner_team_id='t001'
        )

    # 検索画面のテスト
    def test_search_form(self):
        response = self.client.get('/ref/search/')  

        self.assertEqual(response.status_code, 200) # レスポンスの正常性確認
        self.assertTemplateUsed(response, 'ref_analysis/search_form.html') # テンプレート妥当性確認
        self.assertIn(self.team, response.context['teams']) # チーム取得可否の確認
        self.assertIn(self.referee1, response.context['referees']) # 主審取得可否の確認


    # search_formの正常系テスト
    def test_search_result_success(self):
        response = self.client.get('/ref/result/', {'team_id': 't001', 'referee_id': 'r001', 'term': '3'})

        self.assertEqual(response.status_code, 200) # レスポンスの正常性確認
        self.assertTemplateUsed(response, 'ref_analysis/result.html') # テンプレート妥当性確認
        self.assertEqual(response.context['team_name'], '鹿島アントラーズ') # 検索対象チーム名の確認
        self.assertEqual(response.context['referee_name'], '木村 博之') # 検索対象審判名の確認
        self.assertEqual(response.context['season_from'], 2023) # 検索対象開始シーズンの確認
        self.assertEqual(response.context['season_to'], 2025) # 検索対象終了シーズンの確認
        # 戦績計算の妥当性確認
        stats = response.context['stats'] 
        self.assertEqual(stats['games'], 3) # 試合数
        self.assertEqual(stats['wins'], 2) # 勝利数
        self.assertEqual(stats['draws'], 1) # 引分数
        self.assertEqual(stats['loses'], 0) # 敗北数
        self.assertEqual(stats['goals_for'], 5) # 総得点
        self.assertEqual(stats['goals_against'], 2) # 総失点
        self.assertAlmostEqual(stats['win_rate'], 66.66666666666667) # 勝率
        self.assertAlmostEqual(stats['avg_goals_for'], 1.6666666666666667) # 平均ゴール数
        self.assertAlmostEqual(stats['avg_goals_against'], 0.6666666666666666) # 平均失点数
        self.assertEqual( # 直近5試合
            list(stats['recent_matches']),
            [self.match_2025, self.match_2024, self.match_2023]
        )

    # search_resultの試合0件時テスト
    def test_search_result_no_results(self):
        response = self.client.get('/ref/result/', {'team_id': 't001', 'referee_id': 'r002', 'term': '3'})

        self.assertEqual(response.status_code, 200) # レスポンスの正常性確認
        self.assertTemplateUsed(response, 'ref_analysis/no_result.html') # テンプレート妥当性確認
        self.assertEqual(response.context['team_name'], '鹿島アントラーズ') # 検索対象チーム名の確認
        self.assertEqual(response.context['referee_name'], '池内 明彦') # 検索対象審判名の確認
        self.assertEqual(response.context['season_from'], 2023) # 検索対象開始シーズンの確認
        self.assertEqual(response.context['season_to'], 2025) # 検索対象終了シーズンの確認

    # 検索対象期間のパラメータなしケースのエラー確認
    def test_search_result_no_term_parameter(self):
        response = self.client.get('/ref/result/',{'team_id': 't001','referee_id': 'r001','term': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ref_analysis/error.html')
        self.assertEqual(response.context['error_message'],'必要な項目が入力されていません。')

    # 検索対象審判IDのパラメータなしケースのエラー確認
    def test_search_result_no_referee_parameter(self):
        response = self.client.get('/ref/result/',{'team_id': 't001','referee_id': '','term': '3'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ref_analysis/error.html')
        self.assertEqual(response.context['error_message'],'必要な項目が入力されていません。')

    # 検索対象チームIDのパラメータなしケースのエラー確認
    def test_search_result_no_team_parameter(self):
        response = self.client.get('/ref/result/',{'team_id': '','referee_id': 'r001','term': '3'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ref_analysis/error.html')
        self.assertEqual(response.context['error_message'],'必要な項目が入力されていません。')

    # 検索対象チームが存在しないケースのエラー確認
    def test_search_result_no_team_found(self):
        response = self.client.get('/ref/result/',{'team_id': 'tttt','referee_id': 'r001','term': '3'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ref_analysis/error.html')
        self.assertEqual(response.context['error_message'],'指定されたチームが存在しません。')

    # 検索対象審判が存在しないケースのエラー確認
    def test_search_result_no_referee_found(self):
        response = self.client.get('/ref/result/',{'team_id': 't001','referee_id': 'rrrr','term': '3'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ref_analysis/error.html')
        self.assertEqual(response.context['error_message'],'指定された審判が存在しません。')

    # 検索対象期間の型変換失敗ケースのエラー確認
    def test_search_result_term_cast_fail(self):
        response = self.client.get('/ref/result/',{'team_id': 't001','referee_id': 'r001','term': 'あ'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ref_analysis/error.html')

    # 予期せぬエラー発生時のエラー処理
    def test_search_result_unexpected_error(self):
        # calculate_statsでエラーを発生させるためにモック作成
        with patch('ref_analysis.views.calculate_stats') as mock_calculate_stats:
            mock_calculate_stats.side_effect = Exception('テストエラー')

            response = self.client.get('/ref/result/',{'team_id': 't001','referee_id': 'r001','term': '3'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ref_analysis/error.html' )
        self.assertEqual(response.context['error_message'],'予期せぬエラーが発生しました。')