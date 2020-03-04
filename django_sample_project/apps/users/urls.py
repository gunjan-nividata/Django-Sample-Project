from django.urls import path

from apps.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    UserInfoView
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    # Retrieve user detail with permissions from users id/pk
    path('user/<int:pk>', UserInfoView.as_view(), name="user_permission"),

]
