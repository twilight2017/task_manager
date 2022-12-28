from django.shortcuts import render, redirect
from .models import InvitationCode
from .forms import InvitationCodeForm
from django.utils.timezone import now
from django.contrib import messages


# Create your views here.
# get user ip
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# 验证用户邀请码，邀请码正确则以用户IP设为session key, 值为True，会话持续60s
def code_verify(request):
    session_key = "user_ip_{}".format(get_client_ip(request))
    if request.method == "POST":
        code = request.POST.get("code", "")
        code_obj = InvitationCode.objects.filter(code=code, expire__gt=now()).first()
        if code_obj:
            request.session[session_key] = True
            request.session.set_expire(60)  # 会话有效时间为60s，60s后重新提交邀请码
            messages.add_message(request, messages.SUCCESS, "恭喜你已成功通过验证码验证，本次会话60秒有效")
        else:
            messages.add_message(request, messages.WARNING, "你的邀请码错误或已经过期， 请重新输入")
            if session_key in request.session:
                del request.session[session_key]
    return redirect("/")


# 需要有效会话才能访问内容页面，否则展示输入邀请码的表单
def index(request):
    session_key = "user_ip_{}".format(get_client_ip(request))
    # 如果用户IP地址在session里，且值为True则展示隐藏内容
    if session_key in request.session and request.session[session_key] == True:
        return render(request, "myapp/index.html")
    else:
        form = InvitationCodeForm()
        return render(request, "myapp/index.html", {"form": form,})