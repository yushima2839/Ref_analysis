from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from ref_analysis.models import Teams, Referees, ResultsJ1
from datetime import date


class TeamsModelTestCase(TestCase):
    def setUp(self):
        self.instance = Teams.objects.create(team_id='t001', team_name='鹿島アントラーズ', team_category='1')

    # データの存在有無を検証
    def test_create_data(self):
        obj = Teams.objects.create(team_id='t002', team_name='ガンバ大阪', team_category='1')
        self.assertIsNotNone(obj.team_id)

    # データの参照可否を検証
    def test_retrieve(self):
        obj = Teams.objects.get(team_id=self.instance.team_id)
        self.assertEqual(obj.team_name, '鹿島アントラーズ')
        self.assertEqual(obj.team_category, '1')

    # 参照不可データの検証
    def test_retrieve_nonexsistance_data(self):
        with self.assertRaises(ObjectDoesNotExist):
            Teams.objects.get(team_id='123456')

    # 一意制約確保の検証
    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            Teams.objects.create(team_id='t001', team_name='鹿島アントラーズ', team_category='1')


class RefereesModelTestCase(TestCase):
    def setUp(self):
        self.instance = Referees.objects.create(referee_id='r001', referee_name='木村 博之')

    # データの存在有無を検証
    def test_create_data(self):
        obj = Referees.objects.create(referee_id='r002', referee_name='福島 孝一郎')
        self.assertIsNotNone(obj.referee_id)

    # データの参照可否を検証
    def test_retrieve(self):
        obj = Referees.objects.get(referee_id=self.instance.referee_id)
        self.assertEqual(obj.referee_name, '木村 博之')

    # 参照不可データの検証
    def test_retrieve_nonexsistance_data(self):
        with self.assertRaises(ObjectDoesNotExist):
            Referees.objects.get(referee_id='123456')

    # 一意制約確保の検証
    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            Referees.objects.create(referee_id='r001', referee_name='木村 博之')

class ResultsJ1ModelTestCase(TestCase):

    def setUp(self):
        self.instance = ResultsJ1.objects.create(
            match_id='20250214t001t011',
            match_date=date(2026, 8, 13),
            home_team_id='t001',
            home_team='鹿島アントラーズ',
            away_team_id='t002',
            away_team='ガンバ大阪',
            home_team_goal=2,
            away_team_goal=1,
            referee='木村 博之',
            referee_id='r001',
            season='2026',
            category='1',
            winner_team_id='t001'
        )

    # データの存在有無を検証
    def test_create_data(self):
        obj = ResultsJ1.objects.create(
            match_id='m002',
            match_date=date(2026, 8, 14),
            home_team_id='t003',
            home_team='浦和レッズ',
            away_team_id='t004',
            away_team='FC東京',
            home_team_goal=1,
            away_team_goal=1,
            referee='福島 孝一郎',
            referee_id='r002',
            season='2026',
            category='1',
            winner_team_id=''
        )

        self.assertIsNotNone(obj.match_id)

    # データの参照可否を検証
    def test_retrieve(self):
        obj = ResultsJ1.objects.get(match_id=self.instance.match_id)

        self.assertEqual(obj.home_team, '鹿島アントラーズ')
        self.assertEqual(obj.away_team, 'ガンバ大阪')
        self.assertEqual(obj.home_team_goal, 2)
        self.assertEqual(obj.away_team_goal, 1)
        self.assertEqual(obj.referee, '木村 博之')
        self.assertEqual(obj.season, '2026')
        self.assertEqual(obj.category, '1')
        self.assertEqual(obj.winner_team_id, 't001')

    # 参照不可データの検証
    def test_retrieve_nonexsistance_data(self):
        with self.assertRaises(ObjectDoesNotExist):
            ResultsJ1.objects.get(match_id='123456')

    # 一意制約確保の検証
    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            ResultsJ1.objects.create(
                match_id='20250214t001t011',
                match_date=date(2026, 8, 13),
                home_team_id='t001',
                home_team='鹿島アントラーズ',
                away_team_id='t002',
                away_team='ガンバ大阪',
                home_team_goal=2,
                away_team_goal=1,
                referee='木村 博之',
                referee_id='r001',
                season='2026',
                category='1',
                winner_team_id='t001'
            )