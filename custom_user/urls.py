from django.urls import path
from .views import LoginView, RegisterView, ForgetView, SettingsView, \
    VerifyPassword, ContactUsView, NewsView, LogoutView, FaqView, NewsList, \
    verify_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register-api"),
    path('login/', LoginView.as_view(), name="login-api"),
    path('logout/', LogoutView.as_view(), name="logout-api"),
    path('verify/<str:token>/<int:user_id>/', verify_view, name='verify_view'),

    path('forget/', ForgetView.as_view(), name="forget-api"),
    path('settings/', SettingsView.as_view(), name='settings-api'),
    path('change_passw/', VerifyPassword.as_view(), name="verify-api"),

    path('contactus/', ContactUsView.as_view(), name="contact-api"),
    path('news/', NewsView.as_view(), name="news-api"),
    path('news-list', NewsList.as_view(), name='news' ),
    path('faq/', FaqView.as_view(), name="faq-api"),

]
