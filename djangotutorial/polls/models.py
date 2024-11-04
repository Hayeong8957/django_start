import datetime # Python의 표준 모듈인 datetime 모듈

from django.db import models
from django.utils import timezone # Django의 시간대 관련 유틸리티인 timezone 참조

# Create your models here.
class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date publisher')
  def __str__(self):
    return self.question_text
  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)
  def __str__(self):
    return self.choice_text