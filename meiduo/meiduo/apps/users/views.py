from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView

from . import serializers
from .models import User

from .serializers import CreateUserSerializer

# url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
class VerifyEmailView(APIView):
    """验证邮箱
    目的：获取token, 读取出user_id, 查询出当前要认证的用户，将用户的email_active设置True
    """
    def get(self, request):
        # 获取token
        token = request.query_params.get('token')
        if token is None:
            return Response({'message':'缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 读取出user_id, 查询出当前要认证的用户
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message':'无效token'}, status=status.HTTP_400_BAD_REQUEST)

        # 将用户的email_active设置True
        user.email_active = True
        user.save()

        # 响应结果
        return Response({'message': 'OK'})


class EmailView(UpdateAPIView):
    """添加邮箱"""

    # 指定权限：必须用户登录后才能访问该接口
    permission_classes = [IsAuthenticated]

    # 指定序列化器
    serializer_class = serializers.EmailSerializer

    def get_object(self):
        """在这个方法中返回当前的登录用户的user信息"""
        return self.request.user




# url(r'^user/$', views.UserDetailView.as_view()),
class UserDetailView(RetrieveAPIView):
    """用户基本信息
    1.必须用户登录后才能访问该接口
    2.因为目前前端没有传入主键到视图中，所以RetrieveAPIView中的get_object()方法无法获取到pk，所以重写
    """

    # 指定权限：必须用户登录后才能访问该接口
    permission_classes = [IsAuthenticated]

    # 指定序列化器
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        """在这个方法中返回当前的登录用户的user信息"""
        return self.request.user

    # def get(self, request):
    #     # 得到当前登录用户user信息
    #     # 创建序列化器对象
    #     # 进行序列化
    #     # 将序列化结果响应
    #     pass



# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class UsernameCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, username):
        """
        获取指定手机号数量
        """
        # 判断用户名是否存在：根据用户名在数据库中做统计
        count = User.objects.filter(username=username).count()
        return Response({
            'username': username,
            'count': count
        })

# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class MobileCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, mobile):
        """
        获取指定用户名数量
        """
        # 判断手机号是否存在：统计
        count = User.objects.filter(mobile=mobile).count()
        return Response({
            'mobile': mobile,
            'count': count
        })


class UserCreateView(CreateAPIView):
    """注册
    # 新增（用户数据-->校验-->反序列化-->create()-->save()）：保存用户传入的数据到数据库
    """
    # 指定序列化器
    serializer_class = serializers.CreateUserSerializer
