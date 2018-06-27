from django.db import models

# Create your models here.

class Users(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=80)
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=30)
	age = models.IntegerField(null=True)
	sex = models.CharField(max_length=1,null=True)
	pic = models.CharField(max_length=100,null=True)
	#会员状态和注册时间
	#会员状态0 正常 1禁用
	status = models.IntegerField(default=0)
	addtime= models.DateTimeField(auto_now_add=True)
