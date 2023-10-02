from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import Post, User, Comment
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import PostSerializer, UserSerializer, CommentSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken   
from django.utils.decorators import method_decorator 
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework import viewsets
 
class BlogList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class AuthorList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]


    def perform_create(self, serializer):
        serializer.save(username=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]



class APILogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({status: "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({status: "OK, goodbye"})    


class RegisterApi(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

# @api_view(["POST"])
# def logout(request):
#     if request.method == "POST":
#         request.user.auth_token.delete()
#         return Response({"Message": "You are logged out"}, status = status.HTTP_200_OK)

# @api_view(["POST"])
# def register_user(request):
#     if request.method == "POST":
#         serializer = UserSerializer(data=request.data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def user_login(request):
#     if request.method == "POST":
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = None
#         if "@" in username:
#             try:
#                 user = User.objects.get(email=username)
#             except ObjectDoesNotExist:
#                 pass

#         if not user:
#             user = authenticate(username=username, password=password)

#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key}, status=status.HTTP_200_OK)
#         return Response(
#             {"error": "Invalid Credentialis"}, status=status.HTTP_401_UNAUTHORIZED
#         )


@api_view(["POST"])
def user_login(request):
    if request.method == "POST":
        username = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({"token": token}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.response import Response

# class RestrictedView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(data={"message": "You have access to this restricted content."})