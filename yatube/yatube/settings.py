import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'x0-g_o$bm3^+v_(k(f24ogi&=#jnl0lq8^7=!781^06(kp5y^6'
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',
    'www.dazzy123.pythonanywhere.com',
    'dazzy123.pythonanywhere.com',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Регистрация пакетов
    'sorl.thumbnail',  # pip install sorl-thumbnail
    'debug_toolbar',  # pip install django-debug-toolbar==3.2.4
    # Конец регистрации пакетов

    # Регистрация приложений
    'posts.apps.PostsConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'about.apps.AboutConfig',
    # Конец регистрации приложений
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# IP адреса для работы с Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'yatube.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Собственный контекст процессор {{ greeting }}
                'core.context_processors.greeting.welcome',
                'core.context_processors.get_year.year',
            ],
        },
    },
]

WSGI_APPLICATION = 'yatube.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Если DEBUG = True - выключить валидацию пароля
if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Константы для приложений
MAX_SHOW_POSTS = 10
# Конец констант

# Настройки аутентификации
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'posts:index'
# LOGOUT_REDIRECT_URL = 'posts:index'
# Настройка прокрутки емейл сообщений локально
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# Папка хранения email сообщений
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
# Конец настроек аутентификации

# Обработка ошибки 403
CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

# Кеширование
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
# Конец кеширования
