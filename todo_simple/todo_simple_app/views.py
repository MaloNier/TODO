from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import RoomModel, ChatModel, UserManager, User


## トップページ
def index_func(request):
	return render(request, 'index.html')


## 一般ユーザー登録
def general_signup_func(request):
	if request.method == 'POST':
		new_user_email = request.POST['user_email']
		new_user_password = request.POST['password']

		try:
			User.objects.get(email=new_user_email)
			return render(request, 'general_signup.html', {'error':'このユーザーは登録されています。'})
		except:
			user = User.objects.create_user(email=new_user_email, password=new_user_password)
			return render(request, 'general_signup.html')
	return render(request, 'general_signup.html')


## プライムユーザー登録
def prime_signup_func(request):
	if request.method == 'POST':
		new_user_email = request.POST['email']
		new_password = request.POST['password']
		new_user_first_name = request.POST['first_name']
		new_user_last_name = request.POST['last_name']
		new_user_username = request.POST['username']

		# 重複していたらエラー表示
		try:
			User.objects.get(email=new_user_email)
			return render(request, 'prime_signup.html', {'error':'このユーザーは既に登録されています。'})
		except:
			user = User.objects.create_user(email=new_user_email, password=new_password, first_name=new_user_first_name, last_name=new_user_last_name, username=new_user_username)

			return render(request, 'prime_signup.html')
	return render(request, 'prime_signup.html')


## ログイン
def login_func(request):
	if request.method == 'POST':
		user_email = request.POST['user_email']
		user_password = request.POST['password']
		user = authenticate(request, email=user_email, password=user_password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			return redirect('login')
	return render(request, 'login.html')


### ログアウト
def logout_func(request):
	logout(request)
	return redirect('index')


## ルームをリスト表示
@login_required
def home_func(request):
	room_list = RoomModel.objects.all()
	return render(request, 'home.html', {'room_list':room_list})


## ルーム内
@login_required
def room_func(request, pk):
	room = RoomModel.objects.get(pk=pk)
	chat_list = ChatModel.objects.all()
	return render(request, 'room.html', {'room':room, 'chat_list':chat_list})


## ルーム作成
class RoomCreate(CreateView):
	template_name = 'room_create.html'
	model = RoomModel
	fields = {'title', 'author', 'position_1', 'position_2', 'position_3', 'position_4', 'position_5'}
	success_url = reverse_lazy('home')


## 発言作成
class ChatCreate(CreateView):
	template_name = 'chat_create.html'
	model = ChatModel
	fields = {'room_id', 'content', 'author', 'priority'}
	success_url = reverse_lazy('home')