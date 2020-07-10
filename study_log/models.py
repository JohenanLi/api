from django.db import models

# Create your models here.
class study_log(models.Model):
    id = models.IntegerField('ID',primary_key=True)
    last_log = models.IntegerField('最后学习时长')
    last_study = models.IntegerField('最后一次学习时间戳')
    user = models.IntegerField('用户')
    course = models.IntegerField('最后一次学习的课程')

    class Meta:
        verbose_name = '学习记录'
        verbose_name_plural = verbose_name