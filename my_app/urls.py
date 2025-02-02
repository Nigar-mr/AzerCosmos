from django.urls import path
from .views import HomeView, LoginView, RegisterView, LogoutView, settings, verify_passw, \
    verify_view, ContactView

urlpatterns = [
    path('', HomeView.as_view(), name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:token>/<int:user_id>/', verify_view, name='verify_view'),
    path('verify_passw/<str:token>/<int:user_id>/', verify_passw.as_view(), name='verify_passw'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', settings, name='settings'),
    path('contact-us/', ContactView.as_view(), name='contact_us')

]

# from django.conf.urls import url, include
# # from django.contrib.auth.models import User
# from custom_user.models import MyUser
# from rest_framework import routers, serializers, viewsets
#
# User = MyUser
# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']
#
# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]
