from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path("login/", views.loginPage, name="login"),

    path('sign-up/', views.signUpPage, name="sign-up"),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name = 'accounts/password-reset.html'),
         name="password_reset"),

    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password-reset-complete.html'),
         name="password_reset_complete"),


    path('', views.Home, name="home"),

    path("user/", views.userPage, name="user-profile"),

    path("account/", views.accountSetttings, name="account"),

    path('products/', views.products, name="products"),

    path('customer/<str:pk>/', views.custumer, name="custumer"),


    path('create-order/<str:pk>/', views.createOrder, name="create_order")
    ,
    path('update-order/<str:pk>/', views.updateOrder, name="update_order")
    ,
    path('delete-order/<str:pk>/', views.deleteOrder, name="delete_order"),


    path("logout/", views.logOut, name="logout"),

]
