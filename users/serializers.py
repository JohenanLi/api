# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
        
#         refresh = self.get_token(self.user)

#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['username'] = self.user.username

#         return data


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework.validators import UniqueValidator


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    # 利用drf中的validators验证username是否唯一
    # username = serializers.CharField(required=True, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(),
    #                                                                                     message='用户已经存在')])
    # print(username)
    # password = serializers.CharField(
    #      style={"input_type": "password"},help_text="密码", label="密码", write_only=True,
    #  )
    # print(password, "password")

    def create(self, validated_data):
         user = super(UserRegisterSerializer, self).create(validated_data= validated_data)
         user.set_password(validated_data["password"])
         user.save()
         return user
    class Meta:
         model = User
         fields = ( "username", "password", "last_send_code", "token")



class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列表类
    """
    class Meta:
        model = User
        fields = ("id", "name", "username", "last_send_code", "token")