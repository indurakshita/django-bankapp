from django.urls import path
from .views import home,signup, custom_login, ac_detail, perform_transaction,custom_logout

urlpatterns = [
    path('',home,name="home"),
    path('signup/', signup, name='signup'),
    path('login/', custom_login, name='login'),
    path('ac_detail/', ac_detail, name='ac_detail'),
    path('perform_transaction/', perform_transaction, name='perform_transaction'),
    path('logout',custom_logout,name='logout')
]
