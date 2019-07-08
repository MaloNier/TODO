from django.db import models

### 発言のデータモデル
class ChatModel(models.Model):
	content = models.TextField()				# 発言内容
	author = models.CharField(max_length=50)	# 発言者
	images = models.ImageField(upload_to='')	# 画像
	good = models.IntegerField(null=True, blank=True, default=0)	# いいね数
	good_users = models.TextField(null=True, blank=True, default='')# いいねしたユーザー

### ディスカッションルームのデータモデル
class RoomModel(models.Model):
	# id = models.AutoField(primary_ley=True, default=1)		# ルームID
	title = models.CharField(max_length=30)					# ルーム名
	author = models.CharField(max_length=50)	# 設立者
	images	= models.ImageField(upload_to='')	# 画像
	positions = models.CharField(max_length=100)# 立場