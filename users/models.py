from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
class userProfile(AbstractUser):
    # gender_choices = {
    #     ('male','男'),
    #     ('female','女')
    # }
    
    # birthday = models.DateField('生日',null = True, blank = True)
    # gender = models.CharField('性别',max_length = 100 ,choices = gender_choices,default = 'male')
    # address = models.CharField('地址',max_length = 100,default = '')
    id = models.IntegerField('ID')
    name = models.CharField('昵称',max_length = 50,default = '')
    username = models.CharField('手机号',max_length=12,primary_key=True)
    password = models.CharField('验证码',max_length =100)
    last_send_code = models.IntegerField('最后一次发送验证码时间戳',default='0')
    token = models.CharField(max_length = 200,default='0')

    class Meta:
        verbose_name = '用户个人信息'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.username