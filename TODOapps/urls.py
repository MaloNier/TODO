from django.urls import path
from .views import index_func, general_signup_func, login_func, home_func, logout_func, good_func, RoomCreate, room_func

urlpatterns = [
	path('index/', index_func, name='index'),
	path('general_signup/', general_signup_func, name='general_signup'),
	path('login/', login_func, name='login'),
	path('home/', home_func, name='home'),
	path('logout/', logout_func, name='logout'),
	path('good/<int:pk>', good_func, name='good'),
	path('room_create/', RoomCreate.as_view(), name='room_create'),
	path('room/<int:pk>', room_func, name='room'),
]