from django.urls import path
from .views import index_func, general_signup_func, prime_signup_func, login_func, logout_func, home_func, room_func, RoomCreate, ChatCreate

urlpatterns = [
	path('', index_func, name='index'),
	path('general_signup/', general_signup_func, name='general_signup'),
	path('prime_signup/', prime_signup_func, name='prime_signup'),
	path('login/', login_func, name='login'),
	path('logout/', logout_func, name='logout'),
	path('home/', home_func, name='home'),
	path('room/<int:pk>', room_func, name='room'),
	path('room_create/', RoomCreate.as_view(), name='RoomCreate'),
	path('chat_create/', ChatCreate.as_view(), name='ChatCreate')
]