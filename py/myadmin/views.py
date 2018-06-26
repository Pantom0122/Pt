from django.shortcuts import render
from django.http import HttpResponse
from . models import Users
# Create your views here.

def index(request):
	return render(request,'index.html')
	#render里面有三个参数，分别是request对象 第二个是网页名 第三个是字典数据


def add(request):
	if request.method == 'GET':
		return render(request,'myadmin/user/add.html')
	elif request.method == 'POST':
		info = request.POST.dict()
		del info['csrfmiddlewaretoken']
		print(info)
		aa = upload(request)
		info['pic']=aa
		print(aa)
		

		obj = Users.objects.create(**info)
		print(obj)
		print(info)

		# return HttpResponse('<script>alert("添加成功"):location.href=""'+reverse()'</script>')
		return HttpResponse('123')
		

def upload(request):

	pict = request.FILES.get('pic',None)
	print(pict)
	p = pict.name.split('.').pop()
	print(p)

	import time,random

	filename = str(time.time())+str(random.randint(1,9999))+'.'+p

	destination = open("./static/pics/"+filename,"wb+")
	for chunk in pict.chunks():
		destination.write(chunk)
	destination.close()

	return "/static/pics/"+filename


def list(request):

	# return render(request,'myadmin/user/list.html')
	context = Users.objects.all()
	return render(request,'myadmin/user/list.html',{'userlist':context})
	


