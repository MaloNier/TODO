from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import UserManager, User, Meta, ChatModel, RoomModel


### index.htmlを表示
def index_func(request):
	return render(request, 'index.html')

### 一般ユーザー登録
def general_signup_func(request):
	if request.method == 'POST':
		new_user_email = request.POST['email'] 	# 新規ユーザーメールアドレス
		new_password = request.POST['password']			# 新規ユーザーパスワード

		# 重複していたらエラー表示
		try:
			User.objects.get(email=new_user_email)
			return render(request, 'general_signup.html', {'error':'このユーザーは既に登録されています。'})
		except:
			user = User.objects.create_user(email=new_user_email, password=new_password)
			return render(request, 'general_signup.html')
	return render(request, 'general_signup.html')

### ログイン
def login_func(request):
	if request.method == 'POST':
		login_username = request.POST['username']
		#login_user_email = request.POST['mail_address']
		login_password = request.POST['password']

		user = authenticate(request, username=login_username, password=login_password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			return redirect('login')
	return render(request, 'login.html')

### Home表示
@login_required
def home_func(request):
	room_list = RoomModel.object.all()
	return render(request, 'home.html', {'room_list': room_list})

### ログアウト
def logout_func(request):
	logout(request)
	return redirect('login')

### いいね機能
def good_func(request, pk):
	chat = ChatModel.objects.get(pk=pk)
	good_user = request.user.get_username()
	if good_user in chat.good_users:
		return redirect('room')
	else:
		chat.good += 1
		chat.good_users = chat.good_users + ',' + good_user
		chat.save()
		return redirect('room')

### ルーム作成
class RoomCreate(CreateView):
	template_name = 'room_create.html'
	model = RoomModel
	field = {'title', 'author', 'images', 'positinos'}
	success_url = reverse_lazy('home')

@login_required
def room_func(request, pk):
	room = RoomModel.objects.get(pk=pk)
	return(request, 'room.html', {'object': object})