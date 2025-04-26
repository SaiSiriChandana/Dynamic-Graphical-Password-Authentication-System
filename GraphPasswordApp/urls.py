from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("UserLogin", views.UserLogin, name="UserLogin"),
	       path("Login.html", views.Login, name="Login"),
	       path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),
	       path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),	       
	       path("Register.html", views.Register, name="Register"),
	       path("RegisterAction", views.RegisterAction, name="RegisterAction"),	
	       path("PasswordAction", views.PasswordAction, name="PasswordAction"),
	       path("PasswordAuthAction", views.PasswordAuthAction, name="PasswordAuthAction"),
	       path("Reset.html", views.Reset, name="Reset"),
	       path("ResetAction", views.ResetAction, name="ResetAction"),	
	       path("UpdatePassword", views.UpdatePassword, name="UpdatePassword"),	
	       path("ViewUsers", views.ViewUsers, name="ViewUsers"),	
]