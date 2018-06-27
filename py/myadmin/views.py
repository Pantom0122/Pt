from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from . models import Users
# from django.core.urlresolvers import reverse
import os
# Create your views here.

def index(request):
	#从数据库获取用户的数据
	userlist = Users.objects.all()
	#
	return render(request,'index.html',{'userlist':userlist})
	#render里面有三个参数，分别是request对象 第二个是网页名 第三个是字典数据

def add(request):
	#判断
	if request.method == 'GET':
		return render(request,'myadmin/user/add.html')
	elif request.method == 'POST':
		try:
			info = request.POST.copy().dict()
			del info['csrfmiddlewaretoken']

			if request.FILES.get('pic',None):
				info['pic'] = uploads(request)
			else:
				del info['pic']

			obj = Users.objects.create(**info)
			print(obj)
			print(info)
			return HttpResponse('<script>alert("添加成功");location.href="'+reverse('mylist')+'"</script>')
		except:
			return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadd')+'"</script>')

def upload(request):
	#加载图片
	pict = request.FILES.get('pic',None)
	print(pict)
	p = pict.name.split('.').pop()
	print(p)
	# arr = ['jpg','png','jpeg','gif']
 #    if p not in arr:
 #        return 1


	import time,random

	filename = str(time.time())+str(random.randint(1,9999))+'.'+p

	destination = open("./static/pics/"+filename,"wb+")
	for chunk in pict.chunks():
		destination.write(chunk)
	destination.close()

	return "/static/pics/"+filename

def list(request):
	# 获取搜索条件
    types = request.GET.get('type',None)
    keywords = request.GET.get('keywords',None)

    # 判断是否具有搜索条件

    if types:
        # 有搜索条件
        if types == 'all':
            # 全条件搜索
            # select * from user where username like '%aa%' 
            from django.db.models import Q
            userlist = Users.objects.filter(
                Q(username__contains=keywords)|
                Q(age__contains=keywords)|
                Q(email__contains=keywords)|
                Q(phone__contains=keywords)|
                Q(sex__contains=keywords)
            )
        elif types == 'username':
            # 按照用户名搜索
            userlist = Users.objects.filter(username__contains=keywords)
        
        elif types == 'age':
            # 按照年龄搜索
            userlist = Users.objects.filter(age__contains=keywords)

        elif types == 'email':
            # 按照 email 搜索
            userlist = Users.objects.filter(email__contains=keywords)

        elif types == 'phone':
            # 按照 phone 搜索
            userlist = Users.objects.filter(phone__contains=keywords)

        elif types == 'sex':
            # 按照 sex 搜索
            userlist = Users.objects.filter(sex__contains=keywords)


    else:
        # 获取所有的用户数据
        userlist = Users.objects.filter()


    # 判断排序条件
    # userlist = userlist.order_by('-id')

    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分页对象,参数1,数据集合,参数2 每页显示条数
    paginator = Paginator(userlist, 10)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    ulist = paginator.page(p)

   
    # 分配数据
    context = {'userlist':ulist}
    
    # 加载模板
    return render(request,'myadmin/user/list.html',context)

def edit(request):
	#接受用户的id 
	uid = request.GET.get('uid',None)
	#根据用户的id去数据库获取对象信息
	ob = Users.objects.get(id=uid)

	if request.method == 'GET':
		context = {'userlist':ob}
		return render(request,'myadmin/user/edit.html',{'userlist':context})

	elif request.method =='POST':
		try:
			ob.username = request.POST['username']
			ob.email = request.POST['email']
			ob.age = request.POST['age']
			ob.sex = request.POST['sex']
			ob.phone = request.POST['phone']


			if request.FILES.get('pic',None):
				if ob.pic:
					os.remove('.'+ob.pic)

				ob.pic = upload(request)

			ob.save()
			return HttpResponse('<script>alert("修改成功");location.href="'+reverse('mylist')+'"</script>')
		except:
			return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myedit')+'"</script>')

def delete(request):
    try:
        uid = request.GET.get('uid',None)
        print(uid)
        ob = Users.objects.get(id=uid)
        print(ob)
        if ob.pic:
            os.remove('.'+ob.pic)
        ob.delete()
        
        data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}

    return JsonResponse(data)

