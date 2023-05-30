from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('upload', views.upload, name = "upload"),
    path('result/<int:document_id>/', views.result, name = "result"),
    path('register', views.register, name = "register"),
    path('login', views.LoginUser.as_view(template_name="register.html"), name = "login"),
    path("logout", views.logout, name= "logout"),
    path("profile", views.profile, name = "profile")
]

urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)