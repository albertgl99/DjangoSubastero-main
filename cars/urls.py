from cars import views
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="index"),
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("car/", views.car, name="car"),
    path("cochesEnviados/", views.cochesEnviados, name="cochesEnviados"),
    path("car/create", views.create_car, name="create_car"),
    path("car/process-image", views.processImage, name="processImage"),
    path("car/<int:car_id>", views.car_detail, name="car_detail"),
    path("car/<int:car_id>/complete", views.complete_car, name="complete_car"),
    path("car/<int:car_id>/delete", views.delete_car, name="delete_car"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.signin, name="signin"),
    path('payment/<int:car_id>/', views.payment, name='payment'),    
    path('aprobarCoche/<int:car_id>/', views.aprobarCoche, name='aprobarCoche'),
    path('pujar/<int:car_id>/', views.pujar, name='pujar'),  

    path('password_reset/', PasswordResetView.as_view(template_name='registration/passReset.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]