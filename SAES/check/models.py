from django.db import models


# Create your models here.
class Userinfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32, unique=True, verbose_name='账户')
    pwd = models.CharField(max_length=32, verbose_name='密码')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = '账户信息'
