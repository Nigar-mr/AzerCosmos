from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import TemplateView, View
from django.contrib.auth import login, authenticate, logout
from django.views import generic
from custom_user.forms import RegisterForm, LoginForm, SettingProfileForm, PasswordChangeForm
from custom_user.models import News

from custom_user.models import MyUser, Verification

user = MyUser


# Create your views here.

def common():
    context = {}
    context['users'] = MyUser.objects.all().count()
    return context


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = common()
        context['news'] = News.objects.all()
        return context


class RegisterView(generic.TemplateView):
    # form_class = RegisterForm
    template_name = 'register.html'

class ContactView(generic.TemplateView):
    template_name = 'contact_us.html'

class LoginView(generic.TemplateView):
    template_name = 'login.html'

def verify_view(request, token, user_id):
    verify = Verification.objects.filter(token=token, user_id=user_id, expire=False).last()
    if verify:
        verify.expire = True
        verify.save()
        verify.user.is_active = True
        verify.user.save()
        login(request, verify.user)
        messages.info(
            request, "Success"
        )
        return redirect('/')
    else:
        return redirect('/')


def login_view(request):

    return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


def settings(request):
    context = {}
    update = request.user
    # profile_img = request.user.
    context['passw_form'] = PasswordChangeForm()

    if request.method == 'GET':
        if update:
            context['setting_profile'] = SettingProfileForm(instance=update, initial={
                "full_name": request.user.get_full_name()
            })

            return render(request, 'settings.html', context)
    else:
        form = SettingProfileForm(request.POST, request.FILES, instance=update, initial={
            "full_name": request.user.get_full_name()
        })
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'settings.html')


class verify_passw(generic.View):
    context = {}
    context['passw_form'] = PasswordChangeForm()

    def get(self, request, user_id, token):
        verify = Verification.objects.filter(
            user_id=user_id,
            token=token,
        ).last()
        if verify:
            context = {}
            context['passw_form'] = PasswordChangeForm()
            return render(request, 'settings.html', context)
        else:
            # return redirect('home')
            return HttpResponse("else")

    def post(self, request, user_id, token):
        verify = Verification.objects.filter(
            user_id=user_id,
            token=token

        ).last()
        if verify:
            if not verify.expire:
                verify.expire = True
                verify.save()
                form = PasswordChangeForm(request.POST)
                if form.is_valid():
                    passowrd = form.cleaned_data.get('new_passw')
                    print(passowrd)
                    verify.user.set_password(passowrd)
                    verify.user.save()

                    return redirect('/')
                else:
                    print('1')
                    return redirect('/')
            else:
                print('2')
                return redirect('/')
        else:
            print('3')
            return redirect('/')


