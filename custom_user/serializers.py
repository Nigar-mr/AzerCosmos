from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import MyUser, News, Faq, ContactUs


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({"message": ["Your username and/or password do not match"]})


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    # confrim_password = serializers.CharField(max_length=100)


# class SettingsSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=20)
#     confrim_password = serializers.CharField(max_length=20)
#     images = serializers.ImageField
#
#     def validate(self, data):
#         """
#         Check that the start is before the stop.
#         """
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError({"password": "Password not match"})
#         return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.save()

        return user

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if MyUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This user already exist."})

        if MyUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This user already exist."})

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password not match"})
        return data


class PasswordChangeSerializer(serializers.Serializer):
    # email = serializers.EmailField()
    image = serializers.ImageField()
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password not match"})
        return data


class NewsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    images = serializers.ImageField()

    class Meta:
        model = News
        fields = ['title', 'description', 'images']


class FaqSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=255)
    answer = serializers.CharField(max_length=255)

    class Meta:
        model = Faq
        fields = ['question', 'answer']


class ContactUsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=50)
    surname = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=50)
    subject = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=255)

    class Meta:
        model = ContactUs
        fields = ['name', 'surname', 'email', 'phone', 'subject', 'message']



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["email", "username"]


class ProfileEditSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    avatar = serializers.ImageField()

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', "avatar"]

class PasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password not match"})
        return data
