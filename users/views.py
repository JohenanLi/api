from .models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
# Create your views here.
import datetime
import json,random
from rest_framework.views import View,APIView
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework_jwt.utils import jwt_encode_handler
class UsersAPIVIew(View):
    def get(self, request):
        """
        @api {get} /api/users/ 获取所有用户信息
        @apiVersion 0.1.0
        @apiName GetUsers
        @apiGroup 用户
        @apiSuccess {String} user.id 用户的id
        @apiSuccess {String} user.name 用户的昵称
        @apiSuccess {String} user.username 用户名(手机号)
        @apiSuccess {String} user.password 用户的验证码(密码)
        @apiSuccess {String} user.last_send_code 用户上次获取验证码时间戳
        @apiSuccessExample {json} success-example
        {
            "id": "1",
            "name": "aaa",
            "username": "12345678901",
            "code": "1234",
            "last_send_code": "20200710"
        }
        """
        queryset = userProfile.objects.all()
        user_list = []
        for user in queryset:
            user_list.append({
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'code': user.password,
                'last_send_code': user.last_send_code
            })
        return JsonResponse(user_list, safe=False)

    def post(self, request):
        """
        @api {post} /api/users/ 添加单个用户
        @apiVersion 0.1.0
        @apiName appendUser
        @apiGroup 用户
        @apiParam {String} username 用户名(手机号)
        @apiParam {String} name 昵称
        @apiParamExample {json} request-example
        {
            "name":"aaa",
            "username":"12345678901
        }
        @apiSuccess {String} user.id 用户的id
        @apiSuccess {String} user.name 用户的昵称
        @apiSuccess {String} user.username 用户名(手机号)
        @apiSuccess {String} user.password 用户的验证码(密码)
        @apiSuccess {String} user.last_send_code 用户上次获取验证码时间戳
        @apiSuccessExample {json} success-example
        {
            "id": "1",
            "name": "aaa",
            "username": "12345678901",
            "code": "1234",
            "last_send_code": "20200710"
        }
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        user_dict = json.loads(json_str,strict = False)

        # 此处详细的校验参数省略
        queryset = userProfile.objects.all()
        user = userProfile.objects.create(
            name = user_dict.get('name'),
            id = len(queryset) +1,
            username = user_dict.get('username'),
            last_send_code = datetime.date.today().strftime('%Y%m%d')
        )
        return JsonResponse({
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'code': user.password,
            'last_send_code': user.last_send_code
        }, status=201)


class UserAPIView(View):
#    def post(self, request):
#        """
#        获取单个用户信息
#        路由： GET  /user/<username>
#        """
#        json_bytes = request.body
#        json_str = json_bytes.decode()
#        user_dict = json.loads(json_str,strict = False)
#        try:
#             user = userProfile.objects.get(username=user_dict.get('username'))
            
#             return JsonResponse({
#                 'id': user.id,
#                 'name': user.name,
#                 'username': user.username,
#                 'code': user.password,
#                 'last_send_code': user.last_send_code
#             })
#        except userProfile.DoesNotExist:
#            return HttpResponse(status=404)

       

   def put(self, request,username):
       """
       @api {put} /api/user/ 修改用户姓名
       @apiVersion 0.1.0
       @apiName 修改用户名字
       @apiGroup 用户
       @apiParam {String} name 用户昵称
       @apiParamExample {json} request-example
       {
           "name":"bbb"
       }
       @apiError {string} error-example
       {
           "message":"用户不存在"
       }
        @apiSuccess {String} user.id 用户的id
        @apiSuccess {String} user.name 用户的昵称
        @apiSuccess {String} user.username 用户名(手机号)
        @apiSuccess {String} user.password 用户的验证码(密码)
        @apiSuccess {String} user.last_send_code 用户上次获取验证码时间戳
        @apiSuccessExample {json} success-example
        {
                "id": "1",
                "name": "aaa",
                "username": "12345678901",
                "code": "1234",
                "last_send_code": "20200710"
        }
       """
       try:
           user = userProfile.objects.get(username=username)
       except userProfile.DoesNotExist:
           return JsonResponse({"message":"用户不存在"})

       json_bytes = request.body
       json_str = json_bytes.decode()
       user_dict = json.loads(json_str)

       # 此处详细的校验参数省略

       user.name = user_dict.get('name')
       user.save()

       return JsonResponse({
           'id': user.id,
           'name': user.name,
           'username': user.username,
           'code': user.password,
           'last_send_code': user.last_send_code
       })

   def delete(self, request, username):
       """
       @api {delete} /api/user/ 删除用户
       @apiVersion 0.1.0
       @apiName 删除用户
       @apiGroup 用户
       @apiParam {String} username 用户名(手机号)
       @apiParamExample {json} request-example
       {
           "username":"12345678901"
       }
       @apiError {string} error-example
       {
           "message":"用户不存在"
       }
       @apiSuccessExample {json} success-example
       {
           "message":"用户已删除"
       }
       """
       try:
           user = userProfile.objects.get(username=username)
       except userProfile.DoesNotExist:
           return JsonResponse({"message":"用户不存在"})

       user.delete()

       return JsonResponse({"message":"用户已删除"})

class CodeAPIView(View):
    
    def get(self,request,username):
        """
        @api {get} /api/code/<username> 获取验证码
        @apiGroup Code
        @apiName 验证码
        @apiVersion 0.1.0
        @apiParam {String} username 用户名(手机号)
        @apiParamExample {json} 参数post示例
        {
            "username":"12345678901"
        }
        @apiError {String} message 发送失败
        @apiErrorExample {json} 错误示例
        {
            "message":"发送失败"
        }
        @apiSuccess {String} message 发送成功
        @apiErrorExample {json} 成功示例
        {
            "message":"发送成功"
        }
        """
        import random

        queryset = userProfile.objects.all()
        user = userProfile.objects.get(username=username)
        
        code = "%04d" %random.randint(0, 9999)
        user.password = code
        user.last_send_code = datetime.date.today().strftime('%Y%m%d')
        user.save()
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest
        import json,random
        def send_sms(template, username):
            client = AcsClient(,,)
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain('dysmsapi.aliyuncs.com')
            request.set_method('POST')
            request.set_protocol_type('http')  # https | http
            request.set_version('2017-05-25')

            # set_action_name 这个是选择你调用的接口的名称，如：SendSms，SendBatchSms等
            request.set_action_name('SendSms')
            # request.set_action_name('QuerySendDetails')

            # 这个参数也是固定的
            request.add_query_param('RegionId', "default")  # 98A66994-3DF4-4FA5-A33F-CCB36EB599D0
            # request.add_query_param('RegionId', "cn-hangzhou")

            request.add_query_param('PhoneNumbers', username)  # 发给谁
            request.add_query_param('SignName', "卧龙丹心产品验证码")  # 签名
            request.add_query_param('TemplateCode', "SMS_195585549")  # 模板编号
            request.add_query_param('TemplateParam', f"{template}")  # 发送验证码内容
            response = client.do_action_with_exception(request)

            return response
        
        template = {
                        'code': code,
                    }
        res = send_sms(template, username=username)#要发送到的号码
        #print(str(res, encoding='utf-8'))
        res_dict = json.loads(res)
        if res_dict.get('Message') == 'OK' and res_dict.get('Code') == 'OK':
            return JsonResponse({"message":"发送成功"})
            #print("成功啦")
        else:
            return JsonResponse({"message":"发送失败"})
            #print("失败啦")


class JwtLoginView(APIView):
    
    def post(self, request, *args, **kwargs):
        """
        
        @api {post} /api/firstLogin/ 首次登陆或token失效后登陆
        @apiGroup Login
        @apiName 首次登陆或token失效后登陆
        @apiVersion 0.1.0
        @apiParam {String} username 用户名(手机号)
        @apiParam {String} password 验证码(密码)
        @apiParamExample {json} 参数示例
        {
            "username":"12345678901"
            "password":"1234"
        }
        @apiError {String} message 错误信息
        @apiErrorExample {json} error-example
        {
            'message': '用户名或验证码错误'
        }
        @apiSuccess {String} token token
        @apiSuccess {String} user.id 用户的id
        @apiSuccess {String} user.name 用户的昵称
        @apiSuccess {String} user.username 用户名(手机号)
        @apiSuccess {String} user.password 用户的验证码(密码)
        @apiSuccess {String} user.last_send_code 用户上次获取验证码时间戳
        @apiSuccessExample {json} success-example
        {
            "token":"eyJ0eXAiOiJqd3RfIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFsZXgiLCJleHAiOjE1OTQzMDM0OTh9.y5K-c7rkMQWLjlJTTZvMKIBNsSZ0s1aHrfywxR9ytkE",
            "id": "1",
            "name": "aaa",
            "username": "12345678901",
            "code": "1234",
            "last_send_code": "20200710"
        }

        """
        username = request.data.get("username")
        password = request.data.get("password")
        user_obj = userProfile.objects.filter(username=username, password=password).exists()
        if not user_obj:
            return JsonResponse({'message': '用户名或验证码错误'})


        import jwt
        import datetime
        salt = "fadsf$@%#%#%gsfdgsdgfd"
        headers = {
            "typ": "jwt_",
            "alg": "HS256",
        }
        payload = {
            "user_id": 111,
            "username": 111,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=14)
        }
        queryset = userProfile.objects.all()
        user = userProfile.objects.get(username=username)
        token = jwt.encode(payload=payload, key=salt, headers=headers).decode("utf-8")
        user.token = token
        user.save()
        return JsonResponse({'token': token,'id': user.id,
           'name': user.name,
           'username': user.username,
           'code': user.password,
           'last_send_code': user.last_send_code})


class JwtAlwaysView(APIView):
    
    def get(self, request, *args, **kwargs):
        """
        @api {get} /api/alwaysLogin/ 使用token登陆(14天)
        @apiGroup Login
        @apiName 使用token登陆(14天)
        @apiVersion 0.1.0
        @apiParam {String} token token
        @apiParam {String} username 用户名(手机号)
        
        @apiParamExample {json} 参数示例
        {
            "token":"eyJ0eXAiOiJqd3RfIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFsZXgiLCJleHAiOjE1OTQzMDM0OTh9.y5K-c7rkMQWLjlJTTZvMKIBNsSZ0s1aHrfywxR9ytkE",
            "username":"12345678901"
        }
        @apiError {String} msg 错误信息
        @apiErrorExample {json} error-example
        {
            'msg': 'token失效',
            'msg': 'token认证失败',
            "msg": "非法token"
        }
        @apiSuccess {String} user.id 用户的id
        @apiSuccess {String} user.name 用户的昵称
        @apiSuccess {String} user.username 用户名(手机号)
        @apiSuccess {String} user.password 用户的验证码(密码)
        @apiSuccess {String} user.last_send_code 用户上次获取验证码时间戳
        @apiSuccessExample {json} success-example
        {
            "id": "1",
            "name": "aaa",
            "username": "12345678901",
            "code": "1234",
            "last_send_code": "20200710"
        }

        """
        # 获取token并验证
        token = request.query_params.get("token")
        import jwt
        from jwt import exceptions
        result = None
        msg = None
        salt = "fadsf$@%#%#%gsfdgsdgfd"
        try:
            result = jwt.decode(token, salt, True)
            username = request.query_params.get("username")
            user = userProfile.objects.get(username=username)
        except exceptions.ExpiredSignatureError:
            msg = "token失效"

        except exceptions.DecodeError:
            msg = "token认证失败"
        except exceptions.InvalidTokenError:
            msg = "非法token"

        if not result:
            return JsonResponse({"msg": msg})

        return JsonResponse({'id': user.id,
           'name': user.name,
           'username': user.username,
           'code': user.password,
           'last_send_code': user.last_send_code})
        
