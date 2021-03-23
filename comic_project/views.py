import random
import datetime
import json
from django.http.response import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from comic_project import models
from django.db.models import Q

# Create your views here.

def start(request):
    return HttpResponseRedirect('/index')

def index(request):
    list = models.List.objects.all()
    type = models.Type.objects.all()
    return render(request,'index.html',{'list':list,'type':type})

def all(request):
    id = request.GET.get('id')
    comics = models.Comic.objects.all()[(int(id)-1)*9:int(id)*9]
    count = int(models.Comic.objects.all().count()/9)+1
    idn = int(id)+1
    idp = int(id)-1
    return render(request,'comic_all.html',{'comic':comics,'id':id,'count':count,'idn':idn,'idp':idp})

def home(request):
    today = datetime.date.today()
    comicf = models.Comic.objects.order_by('?')[1]
    comici = models.Comic.objects.order_by('?')[:2]
    comic = models.Comic.objects.all()[int(today.day):int(today.day)+18]
    return render(request, 'home.html', {'comic':comic,'comici':list(comici),'comicf':comicf})

def login(request):
    return render(request,'login.html',{'status':''})

def login_render(request):
    return render(request,'index.html',{})

def logout(request):
    '''
    退出登录
    :param request:
    :return:
    '''
    request.session.setdefault('username',None)
    request.session['username'] = None
    request.session.setdefault('is_staff',0)
    request.session['is_staff'] = 0
    return HttpResponseRedirect('/')

def register(request):
    return render(request,'register.html',{'status':''})

def login_valid(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username and password:
        try:
            auth_user = models.AuthUser.objects.all().get(username=username)
            auth_password = models.AuthUser.objects.all().get(username=username).password
            if password == auth_password:
                request.session['username'] = auth_user.username
                request.session['is_staff'] = auth_user.is_staff
                return HttpResponseRedirect('/')  # 这里不使用render的方式是由于render方式跳转后，浏览器地址栏的url不会随之变化，可能影响后面的url跳转
            else:
                return render(request,'login.html',{'status': '密码不正确'})
        except:
            return render(request,'login.html',{'status': '账户不存在'})
    else:
        return render(request,'login.html',{'status': '账号或密码为空'})

def register_valid(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    authuser = 'authuser'
    try:
        models.AuthUser.objects.all().get(username=username)
    except:
        authuser = None
    if authuser == None:
        try:
            models.AuthUser.objects.create(username=username, password=password, is_staff=0)
            return HttpResponseRedirect('/login')
        except:
            return render(request,'register.html',{'status':'注册失败'})
    else:
        return render(request,'register.html',{'status':'用户已存在'})

def forget(request):
    return render(request,'register.html',{})


def profile(request):
    username = request.session.get('username')
    user = models.AuthUser.objects.filter(username=username).first()
    collect = models.Collect.objects.filter(username=username)
    count = models.Collect.objects.filter(username=username).count()
    comic = []
    for item in collect:
        m = models.Comic.objects.filter(id=item.cid).first()
        comic.append(m)
    return render(request,'profile.html',{'user':user,'comic':comic,'count':count})

def comic_content(request):
    id = request.GET.get('id')
    print(id)
    comic_type = models.ComicType.objects.filter(tid=id).all()
    comic = []
    for ct in comic_type:
        m = models.Comic.objects.filter(id=ct.cid).first()
        comic.append(m)
    return render(request, 'comic_content.html', {'comic':comic})

def comic_rank(request):
    id = request.GET.get('id')
    print(id)
    comic_type = models.Rank.objects.filter(lid=id).all()
    comic = []
    for ct in comic_type:
        m = models.Comic.objects.filter(id=ct.cid).first()
        comic.append(m)
    return render(request, 'comic_rank.html', {'comic':comic})


def comic_detail(request):
    id = request.GET.get('id')
    coll = models.Collect.objects.filter(Q(username=request.session.get('username'))&Q(cid=id))
    flag = ''
    if len(coll)==0:
        flag = ''
    else:
        flag = '1'
    print(id)
    comic_type = models.ContentIndex.objects.filter(titleid=id).all()
    content = models.Comic.objects.filter(id=id).first()
    comic = []
    for ct in comic_type:
        m = models.Content.objects.filter(id=ct.contentid).first()
        comic.append(m)
    cid = comic[len(comic) - 1].id
    return render(request, 'comic_detail.html', {'comic': comic,'content':content,'cid':cid,'flag':flag})


def comic_final(request):

    id = request.GET.get('id')
    print(id)
    comic_de = models.Content.objects.get(id=id)
    content = models.ComicContent.objects.filter(content_second_id=id)
    comic_id = []
    if len(content) > 0:
        comic_id = models.Comic.objects.get(id=content[0].contentid)

    content_index = models.ContentIndex.objects.filter(titleid=comic_de.cid)
    pre = -1
    next = -1
    for i in range(len(content_index)):
        if int(content_index[i].contentid) == int(id):
            if i == 0 and i == len(content_index)-1:
                pre = -1
                next = -1
            elif i == 0 and i!= len(content_index)-1:
                pre = -1
                next = content_index[i+1].contentid
            elif i!= 0 and i!= len(content_index)-1:
                pre = content_index[i-1].contentid
                next = content_index[i+1].contentid
            else:
                pre = content_index[i-1].contentid
                next = -1

    return render(request, 'comic_final.html', {'content': content,'comic':comic_id,'comic_de':comic_de,'pre':pre,'next':next})

def search(request):
    id = request.POST.get('text')
    comic = models.Comic.objects.filter(Q(name__contains=id)|Q(author__contains=id))
    return render(request, 'search_results.html', {'comic':comic})

@csrf_exempt
def addfoucs(request):
    id = request.POST.get('id')
    username = request.session.get('username')
    obj = models.Collect(username=username,cid=id)
    obj.save()
    return HttpResponse(json.dumps({'status': 'success'}))

@csrf_exempt
def removefoucs(request):
    id = request.POST.get('id')
    username = request.session.get('username')
    models.Collect.objects.filter(Q(username=username)&Q(cid=id)).delete()
    return HttpResponse(json.dumps({'status': 'success'}))

def form_v(request):
    username = request.session.get('username')
    user = models.AuthUser.objects.get(username=username)
    return render(request,'form_validate.html',{'user':user})

def form_c(request):
    username = request.GET.get('username')
    print(username)
    user = models.AuthUser.objects.get(username=username)
    return render(request,'form_change.html',{'user':user})

def form_valid(request):
    username = request.session.get('username')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    print(username,firstname,lastname,password,email,phone)

    models.AuthUser.objects.filter(username=username).update(first_name=firstname,last_name=lastname,password=password,email=email,phone=phone)
    return HttpResponse(json.dumps({'status': 'success'}))

def form_change(request):
    username = request.POST.get('username')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    print(username,firstname,lastname,password,email,phone)

    # models.AuthUser.objects.filter(username=username).update(first_name=firstname,last_name=lastname,password=password,email=email,phone=phone)
    return HttpResponse(json.dumps({'status': 'success'}))

def change(request):
    users = models.AuthUser.objects.filter(is_staff=0)
    return render(request,'change.html',{'users':users})

def delete_user(request):
    id = request.POST.get('id')
    models.AuthUser.objects.filter(id=id).delete()
    return HttpResponse(json.dumps({'status': 'success'}))
