from django.db import models

# Create your models here.
class Teams(models.Model):
    # チームID
    team_id = models.CharField(max_length=50, primary_key=True)
    # チーム名
    team_name = models.CharField(max_length=50)
    # チームカテゴリ
    team_category = models.CharField(max_length=50)

    class Meta:
        managed = False  # 既存DBなので Django に作らせない
        db_table = 'teams'

    def __str__(self):
        return self.team_name

class Referees(models.Model):
    # 主審ID
    referee_id = models.CharField(max_length=50, primary_key=True)
    # 主審名
    referee_name = models.CharField(max_length=50)

    class Meta:
        managed = False  
        db_table = 'referees'

    def __str__(self):
        return self.referee_name

class ResultsJ1(models.Model):
    # 試合ID
    match_id = models.CharField(max_length=50, primary_key=True)
    # 試合開催日
    match_date = models.DateField()
    # ホームチームID
    home_team_id = models.CharField(max_length=50)
    # ホームチーム名
    home_team = models.CharField(max_length=50)
    # アウェイチームID
    away_team_id = models.CharField(max_length=50)
    # アウェイチーム名
    away_team = models.CharField(max_length=50)
    # ホームチームゴール数
    home_team_goal = models.IntegerField()
    # アウェイチームゴール数
    away_team_goal = models.IntegerField()
    # 主審名
    referee = models.CharField(max_length=50)
    # 主審ID
    referee_id = models.CharField(max_length=50)
    # シーズン
    season = models.CharField(max_length=10)
    # カテゴリ
    category = models.CharField(max_length=1)
    # 勝利チームID
    winner_team_id = models.CharField(max_length=50)

    class Meta:
        managed = False  # 既存DBなので Django に作らせない
        db_table = 'results_J1'


    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.referee}"
    
