from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, analytics_chart
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
path('bokeh_office_summary/', views.bokeh_office_summary, name='bokeh_office_summary'),
    path('plotly_max_balance/', views.plotly_max_balance, name='plotly_max_balance'),
    path('bokeh_max_balance/', views.bokeh_max_balance, name='bokeh_max_balance'),
    path('plot_bokeh_balance/', views.plot_bokeh_balance, name='plot_bokeh_balance'),  # Add this line
    path('plot_plotly_balance/', views.plot_plotly_balance, name='plot_plotly_balance'),
    path('user_balance/', views.user_balance_view, name='user_balance_view'),  # To handle the User ID form

    path('bokeh_above_average_balance/', views.bokeh_above_average_balance, name='bokeh_above_average_balance'),
    path('plotly_above_average_balance/', views.plotly_above_average_balance, name='plotly_above_average_balance'),
    # Other URL patterns...
    path('bokeh_operations_summary/', views.bokeh_operations_summary, name='bokeh_operations_summary'),
    path('plotly_operations_summary/', views.plotly_operations_summary, name='plotly_operations_summary'),
    path('bokeh_detailed_operations/', views.bokeh_detailed_operations, name='bokeh_detailed_operations'),
    path('plotly_detailed_operations/', views.plotly_detailed_operations, name='plotly_detailed_operations'),

    path('analytics_chart/', views.analytics_chart, name='analytics_chart'),

]
