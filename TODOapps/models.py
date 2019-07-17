from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


### ユーザーモデルのカスタム
# ユーザーマネージャー
class UserManager(BaseUserManager):

	use_in_migrations = True	# クラスをRUｎPython操作で利用できるように

	def _create_user(self, email, password, first_name, last_name, username, **extra_fields):
		'''メールアドレスでの登録を必須に'''
		if not email:
			raise ValueError('メールアドレスの登録は必須です。')
		email = self.normalize_email(email)

		user = self.model(email=email, first_name=first_name, last_name=last_name, username=username, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, first_name=None, last_name=None, username=None, **extra_fields):
		'''管理者権限全般をFalseに'''
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		'''スーパーユーザーは管理者権限全般をTrueに'''
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)

# カスタマイズユーザーモデル
class User(AbstractBaseUser, PermissionsMixin):

	email = models.EmailField(_('email_address'), unique=True)	# ユーザーのメールアドレスは一意に
	first_name = models.CharField(_('first name'), max_length=30, blank=True)	# ユーザの実名(姓)
	last_name = models.CharField(_('last name'), max_length=100, blank=True)	# ユーザーの実名(名)
	username = models.CharField(_('user name'), max_length=100, blank=True)		# ユーザーのハンドルネーム
	is_prime = models.BooleanField(
		_('prime'),
		default=False,
		help_text=_(
			'実名登録による制限解除を行うかどうかを指定します。'
		),
	)

	is_staff = models.BooleanField(
		_('staff_status'),
		default=False,
		help_text=_(
			'ユーザーが管理者画面にログイン出来るかを指定します。'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'このユーザーをアクティブとして扱うべきかどうかを指定します。'
			'アカウントを削除する代わりにこの選択を解除してください。'
		),
	)
	date_joined = models.DateTimeField(_('data joined'), default=timezone.now)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []


class Meta:
	verbose_name = _('user')
	verbose_name_plural = _('users')

def get_full_name(self):
	'''Return the first_name plus the last_name, with a space in
	between.'''
	full_name = '%s %s' % (self.first_name, self.last_name)
	return full_name.strip()

def get_short_name(self):
	'''Return the short name for the user.'''
	return self.first_name

def email_user(self, subject, message, from_email=None, **kwargs):
	'''Send an email to this user.'''
	send_mail(subject, message, from_email, [self.email], **kwargs)

@property
def username(self):
	'''username属性のゲッター

	他アプリケーションが、username属性にアクセスした場合に備えて定義
	メールアドレスを返す
	'''
	return self.email


### 発言のデータモデル
class ChatModel(models.Model):
	content = models.TextField()				# 発言内容
	author = models.CharField(max_length=50)	# 発言者
	images = models.ImageField(upload_to='')	# 画像
	good = models.IntegerField(null=True, blank=True, default=0)	# いいね数
	good_users = models.TextField(null=True, blank=True, default='')# いいねしたユーザー

	USERNAME_FIELD = ''
	REQUIRED_FIELDS = []

### ディスカッションルームのデータモデル
class RoomModel(models.Model):
	# id = models.AutoField(primary_ley=True, default=1)		# ルームID
	title = models.CharField(max_length=30)					# ルーム名
	author = models.CharField(max_length=50)	# 設立者
	images	= models.ImageField(upload_to='')	# 画像
	positions = models.CharField(max_length=100)# 立場

	USERNAME_FIELD = ''
	REQUIRED_FIELDS = []