"""
Django settings for rainsystem project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import subprocess
import socket
# from backend.dehazing.test import create_dehazingModel
# from backend.derain.load_model import createMoss
# import backend.textspot.mmocr.init_text_model as InitTextModel

import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()

# Models

RESOURCE_PORT = "8095"
RESOURCE_IP_PORT = "http://10.109.246.53:" + RESOURCE_PORT
p = subprocess.Popen('ps -ef | grep ' + RESOURCE_PORT + " | grep -v grep", shell=True)
text = p.communicate()
if text is None or len(text) == 0 or text[0] is None:
    s = subprocess.Popen("python -m http.server " + RESOURCE_PORT, shell=True, close_fds=True)
BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCE_RELATIVE_PATH = 'backend/resources/'
RESOURCE_ROOT = os.path.join(BASE_DIR, RESOURCE_RELATIVE_PATH)
# MODEL_DIRECTORY = {
#     0: 'tmp',
#     1: 'deraining',
#     2: 'dehazing',
#     3: 'deblurring',
#     4: 'enhance',
#     5: 'textdetection',
#     6: 'derainingThenTextdetection',
#     7: 'dehazingThenTextdetection'
# }
CHANNELS_SRC = {
    0: 1,
}
CHANNELS_RES = {
    1: 2,
    2: 2,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 3,
}
# HOST = IP + ":10800"
#print(IP)
# RESOURCE_HOST = IP + ":" + VIDEO_PORT + "/resources"
#print(RESOURCE_HOST)
USER = 'admin'
PASSWORD = 'admin'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8bfa=$oeqd7f+4n5=3w$r!^5zvn09rfplf%61u=70kxnya1y_6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'rainsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rainsystem.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rainsystem',
        'USER': 'rc',
        'PASSWORD': '',
        'HOST': '10.109.246.53',
        'PORT': '3307',
        'OPTIONS': {
            'autocommit': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 开启debug模式，注意上线运营时要关闭debug
DEBUG = True
# 允许所有ip访问
ALLOWED_HOSTS = ['*']
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# 允许所有的请求头
CORS_ALLOW_HEADERS = ('*')


EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议（用于在两个通信应用之间提供保密
EMAIL_HOST = 'smtp.163.com'  # 发送邮件的邮箱 的SMTP服务器
EMAIL_PORT = 25  # 发件箱的STMP服务器端口
EMAIL_HOST_USER = 'imissrc@163.com'  # 帐号，发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'rc123456'  # 授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 收件人看到的发件人

# load dao
# dehazing_model = create_dehazingModel()
# os.environ['CUDA_VISIBLE_DEVICES'] = '1'
derain_moss_model = None
# derain_moss_model = createMoss()
# mmocr_model = InitTextModel.build_mmocr_model()   # 初始化一个MMOCR类
