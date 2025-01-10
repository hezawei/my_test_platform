from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/manage/')

    #返回登录页面
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        if username == "" or password == "":
            return render(request, "login.html", {
                "error": "用户名或密码为空！"
            })
        # authenticate 函数来验证用户提供的用户名和密码是否匹配。
        # 它会尝试根据传入的 username 和 password 参数，在数据库（默认是 auth_user 表）中查找对应的用户记录，并验证密码是否正确。
        user = auth.authenticate(username=username, password=password)
        if user:
            # login 函数实际完成用户登录的操作, 它会在当前的请求会话（Session）中记录用户的登录状态
            auth.login(request, user)
            response = HttpResponseRedirect("/manage/")
            response.set_cookie("user", username, max_age=3600)
            return response
        else:
            return render(request, "login.html", {
                "error": "用户名或密码错误"
            })


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")