from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('userreg/', views.userreg, name='userreg'),  # сторінка реєстрації
    path('insertuser/', views.insertuser, name='insertuser'),  # обробка додавання користувача
    path('user_profile/', views.user_profile, name='user_profile'),  # сторінка профілю користувача
    path('user_extract/', views.userextract, name='userextract'),  # сторінка виписки
    path('userlog/', views.userlog, name='userlog'),  # сторінка входу
    path('loginuser/', views.loginuser, name='loginuser'),  # обробка входу
    # Інші ваші маршрути
    path('transfer_funds/<int:sender_id>/', views.transfer_funds, name='transfer_funds'),
    path('delete_account/', views.delete_current_user, name='delete_account'),
    path('', include(router.urls)),
]
