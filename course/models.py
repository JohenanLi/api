from django.db import models

# Create your models here.
class course(models.Model):
    course_id = models.IntegerField("课程ID")
    course_name = models.CharField("课程标题",max_length = 50)
    description = models.CharField("课程描述",max_length = 300)
    length = models.IntegerField("课程长度")
    path = models.CharField("课程源地址",max_length = 500)
    image = models.CharField("图片源地址",max_length = 500)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name