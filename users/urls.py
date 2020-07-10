from django.urls import path
from . import views
from . import serializers
urlpatterns = [
   path('api/users/', views.UsersAPIVIew.as_view(),name='全部用户操作'),
   path('api/user/', views.UserAPIView.as_view(),name='单个用户操作'),
   path('api/code/<username>',views.CodeAPIView.as_view(),name='验证码'),
#    # 认证令牌
#    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#    # 刷新令牌
#    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
# #    path('api/login/', serializers.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/firstLogin/',views.JwtLoginView.as_view()),
    path('api/alwaysLogin/',views.JwtAlwaysView.as_view())


]
