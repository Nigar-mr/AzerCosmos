import json
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.signals import user_logged_out

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer, LoginUserSerializer, ProfileSerializer, \
    EmailVerificationSerializer, PasswordChangeSerializer, ContactUsSerializer, NewsSerializer, \
    FaqSerializer, RegisterSerializer, ProfileEditSerializer
from .models import MyUser, ContactUs, News, Faq
from .tools.params import auth_header
from .permission import IsAdminUser, IsLoggedInUserOrAdmin, IsAdminOrAnonymousUser
from custom_user.models import Verification


class UserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAdminOrAnonymousUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer
    print('1')
    @swagger_auto_schema(tags=["Authorization"], operation_id="login", responses={
        400: "Bad request"
    })
    def post(self, request, *args, **kwargs):
        print('asd')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print('gd')
            user = serializer.validated_data
            print(user)
            _, token = AuthToken.objects.create(user)
            print(token)
            return Response({
                "user": ProfileSerializer(user, context=self.get_serializer_context()).data,
                "token": token
            }, status=200)
        else:
            err = [f"{self.to_camel_case(key)}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({
                "detail": err[0]
            }, status=400)

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0].title() + ''.join(x.title() for x in components[1:])


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["Authorization"], operation_id="logout", responses={
        401: "Invalid token."
    }, manual_parameters=[auth_header])
    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response({
            "detail": "Success"
        }, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(tags=["Register"], operation_id="register", responses={
        400: "Bad request"
    })
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            surname = serializer.validated_data['surname']
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            MyUser.objects.create(
                first_name=name, last_name=surname, username=username, email=email,
                password=password
            )

            return Response({
                "email": email,
                "detail": "Please check your email address for verification code."
            }, status=status.HTTP_200_OK)

        else:
            err = [f"{self.to_camel_case(key)}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({
                "detail": err[0]
            }, status=400)

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0].title() + ''.join(x.title() for x in components[1:])


class ForgetView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmailVerificationSerializer

    @swagger_auto_schema(tags=["Forget Password"], operation_id="forget", responses={
        400: "Bad request"
    })
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = MyUser.objects.filter(email=email).last()
            if user:
                Verification.objects.create(
                    user=user
                )
                return Response({
                    "email": email,
                    "detail": "Please check your email address for verification code."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "detail": "Can't find user this email address"
                }, status=400)
        else:
            err = [f"{self.to_camel_case(key)}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({
                "detail": err[0]
            }, status=400)

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0].title() + ''.join(x.title() for x in components[1:])


class VerifyPassword(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordChangeSerializer

    @swagger_auto_schema(tags=["Change Password"], operation_id="change_passw", responses={
        400: "Bad request"
    })
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            email = request.user
            password = serializer.validated_data['password']
            verify = Verification.objects.filter(user__email=email, expire=False).last()

            if verify:
                if not verify.expire:
                    verify.expire = True
                    verify.save()
                    user = verify.user
                    user.set_password(password)
                    user.save()
                    return Response({
                        "detail": "Password successfuly change"
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({
                        "detail": "Code: Verification code is expired"
                    }, status=400)
            else:
                return Response({
                    "detail": "Code: Verification code is not valid"
                }, status=400)
        else:
            err = [f"{self.to_camel_case(key)}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({
                "detail": err[0]
            }, status=400)

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0].title() + ''.join(x.title() for x in components[1:])


class SettingsView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProfileEditSerializer

    @swagger_auto_schema(tags=["Profile Info/Update"], operation_id="image-upload", manual_parameters=[auth_header],
                         request_body=ProfileEditSerializer)
    def put(self, request, *args, **kwargs):
        serializer = ProfileEditSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            user = serializer.save()
            return Response(ProfileSerializer(user).data)
        else:
            err = [f"{self.to_camel_case(key)}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({
                "detail": err[0]
            }, status=400)

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0].title() + ''.join(x.title() for x in components[1:])


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
        return JsonResponse({
            "status": "OK"
        })
    else:
        return JsonResponse({
            "status": 404
        })


@csrf_exempt
def main_index(request):
    if request.method == "GET":
        return JsonResponse({
            "status": "OK"
        })
    else:
        return JsonResponse({
            "type_of_request": request.method
        })


@csrf_exempt
def api_main_news(request):
    if request.method == "GET":
        news_list = News.objects.all()
        arr = []
        for news in news_list:
            arr.append({
                "title": news.title,
                "content": news.content
            })
        return JsonResponse(arr, safe=False)
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        if "title" in data and "content" in data:
            news = News.objects.create(
                title=data.get("title"),
                content=data.get("content")
            )
            return JsonResponse({
                "id": news.id,
                "title": news.title,
                "content": news.content
            }, status=201)


@csrf_exempt
def api_news_update(request, id):
    news = News.objects.filter(id=id).last()
    if news:
        if request.method == "GET":
            return JsonResponse({
                "id": news.id,
                "title": news.title,
                "content": news.content
            })

        elif request.method == "PUT":
            data = json.loads(request.body.decode("utf-8"))
            news.title = data.get("title", news.title)
            news.content = data.get("content", news.content)
            news.save()
            return JsonResponse({
                "id": news.id,
                "title": news.title,
                "content": news.content
            }, status=201)
        elif request.method == "DELETE":
            old_news = news
            news.delete()
            return JsonResponse({
                "id": old_news.id,
                "title": old_news.title,
                "content": old_news.content
            })
    else:
        return JsonResponse({
            "message": "Not found news"
        })


#TODO You are authenticated as nigar-muradli@mail.ru, but are not authorized to access this page. Would you like to login to a different account?

class NewsList(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = News.objects.all()
        return qs
    @swagger_auto_schema(tags=["News get"], operation_id="news", responses={
        500: "Server error"
    })

    def get(self, request, *args, **kwargs):
        return super(NewsList, self).get(request, *args, **kwargs)



class NewsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = NewsSerializer

    @swagger_auto_schema(tags=["News"], operation_id="news", responses={
        400: "Bad request",
        401: "Unauthorized",
    }, manual_parameters=[auth_header], request_body=NewsSerializer)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            description = serializer.validated_data['description']
            images = serializer.validated_data['images']
            created_by = request.user
            News.objects.create(
                title=title, description=description, images=images, created_by=created_by)

            return Response({
                "title": title,
                "detail": "Create News post succesfully"
            }, status=status.HTTP_200_OK)

    def put(self, request):
        news = News.objects.filter(id=id).last()
        data = json.loads(request.body.decode("utf-8"))
        news.title = data.get("title", news.title)
        news.description = data.get("description", news.description)
        news.save()
        return JsonResponse({
            "id": news.id,
            "title": news.title,
            "content": news.content
        }, status=201)

    def delete(self, request):
        news = News.objects.filter(id=id).last()
        old_news = news
        news.delete()
        return JsonResponse({
            "id": old_news.id,
            "title": old_news.title,
            "description": old_news.description
        })


class FaqView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FaqSerializer

    @swagger_auto_schema(tags=["Faq"], operation_id="faq", responses={
        200: FaqSerializer,
        400: "Bad request",
        401: "Unauthorized",
    }, manual_parameters=[auth_header], request_body=FaqSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            answer = serializer.validated_data['answer']
            Faq.objects.create(
                question=question, answer=answer)

            return Response({
                "title": question,
                "detail": "Create Faq post succesfully"
            }, status=status.HTTP_200_OK)

    def put(self, request):
        faq = Faq.objects.filter(id=id).last()
        data = json.loads(request.body.decode("utf-8"))
        faq.question = data.get("question", faq.question)
        faq.answer = data.get("answer", faq.answer)
        faq.save()
        return JsonResponse({
            "id": faq.id,
            "question": faq.question,
            "answer": faq.answer
        }, status=201)

    def delete(self, request):
        faq = Faq.objects.filter(id=id).last()
        old_faq = faq
        faq.delete()
        return JsonResponse({
            "id": old_faq.id,
            "title": old_faq.question,
            "description": old_faq.answer
        })


class ContactUsView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContactUsSerializer
    print('1')
    @swagger_auto_schema(tags=['Contact Us'], operation_id='contact', response={
        400: "Bad request"
    })
    def post(self, request, *args, **kwargs):
        print('2')
        serializer = self.get_serializer(data=request.data)
        print('3')
        if serializer.is_valid():
            print('4')
            email = serializer.validated_data['email']
            name = serializer.validated_data['name']
            surname = serializer.validated_data['surname']
            phone = serializer.validated_data['phone']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            ContactUs.objects.create(
                email=email, name=name, surname=surname, phone=phone, subject=subject, message=message
            )
            return Response({
                "email": email,
                "detail": "Please check your email address for verification code."
            }, status=status.HTTP_200_OK)

        else:
            err = [f"{self.to_camel_case(key)}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({
                "detail": err[0]
            }, status=400)
