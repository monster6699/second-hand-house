from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from house.utils.models import BaseModel
# from info.models import House
from info.models import House


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True,verbose_name='手机号')
    email_active = models.BooleanField(default=False)
    class Meta:
        db_table = 'tb_users'
        verbose_name='用户',
        verbose_name_plural=verbose_name


class Follow(models.Model):
    user = models.ForeignKey(User,related_name='follow',on_delete=models.CASCADE)
    house = models.ForeignKey(House,related_name='follow',on_delete=models.CASCADE)
    class Meta:
        db_table = 'tb_follow'
        verbose_name='关注表',
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.user.id
