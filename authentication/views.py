
from rest_framework import status, generics, permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import SignUpSerializer, ProfileSerializer, ChangePasswordSerializer
from .models import User, UserProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSignInSerializer


class SignUp(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head', 'post']
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        status_code: int = 0
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'User registered  successfully',
                "user": serializer.data
            }
            return Response(response)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            error_response = {

                'success': False,
                'status_code': status_code,
                'message': 'Username or email exists',
            }
            return Response(error_response)


class SignIn(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        status_code: int = 0

        if serializer.is_valid():
            status_code = status.HTTP_200_OK
            user = User.objects.get(email=serializer.data['email'])
            print(serializer.data)
            # exp = datetime.datetime.utcnow() +

            # login(request, request.data['email'], request.data['password'] )
            response = {
                'success': True,
                'status code': status_code,
                'message': 'User logged in  successfully',
                'token': serializer.data['token'],
                # 'exp': str(exp),
                'user': {
                    'id': str(user.id),
                    'username': str(user.username),
                    'email': str(user.email)
                }
            }

            return Response(response, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'status code': status_code,
                'error': f'Username or Password is incorrect',
            }
            return Response(response, status=status_code)


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication

    def get(self, request, *args, **kwargs):
        try:

            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'User profile fetched successfully',
                'data': {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    'image': user_profile.get_imag_url
                }
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


class ChangePasswordView(generics.UpdateAPIView):
    """ An endpoint for changing password."""
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JWTAuthentication

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            """ 
            We need to check the old password if it vs
               the same as the user entered
            """
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {

                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





