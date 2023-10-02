from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from api import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", views.BlogList.as_view()),
    path("blog/", views.BlogList.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("blog/blogs/", views.BlogList.as_view(), name="blogs"),
    path("blog/<int:pk>/", views.BlogDetail.as_view(), name="blog-detail"),
    path("blog/bloggers/", views.AuthorList.as_view(), name="author-list"),
    path("blog/blogger/<int:pk>/", views.AuthorDetail.as_view(), name="author-detail"),
    path("comments/", views.CommentList.as_view(), name="comment"),
    path("comments/<int:pk>/", views.CommentDetail.as_view()),
    # path("register/", views.register_user, name="register"),
    # path("login/", views.user_login, name="login"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout_token/", views.APILogoutView.as_view(), name="logout_token"),
    path("api/register/", views.RegisterApi.as_view()),
    # path("login/", obtain_auth_token, name="login"),
    # path("logout/", views.logout(),name='logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
