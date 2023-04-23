"""
Django settings for radioamador project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=i90n-bvj_b-zfp3svjr^k6*0^@v2ggztps+t_sd56%%=4cby&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Se debug = False, temos que especificar um host que hospedará a aplicação, como o Heroku, AWS etc... Sempre use debug = False em um server de produção.

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    
    #  My Apps
    'indicativo',  
    'users',  
    
    # Third party Apps
    'bootstrap5',
    
    #  Standard Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'radioamador.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'error_handlers')],  #  Em um ambiente de produção, com o Debug = True, deve ser configurado um código para a app gerenciar os templates handlers
        'APP_DIRS': True,  # Depois de hospedar, faça um migrate e sua app irá acessar o db.
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

WSGI_APPLICATION = 'radioamador.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Quando fazer o deploy, aqui vc coloca o hostname, porta, username, password e o nome do database do server.
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/img/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # Isso aqui mostra ao Dingo onde procurar ao trabalhar com imagens.
    
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# My configs
LOGIN_URL = 'users:login'

# django-bootstrap5 configs
BOOTSTRAP = {
    'include_jquery': True,
}

# Heroku configs

if os.getcwd() == '/app':  #  Permite a app ser rodada no server Heroku ao invés do localhos/Baofeng.
    import dj_database_url  #  Ajuda o Heroku administrar o DB, O heroku usa o postgre por padrão, então há uma transcrição do nosso db para esse dialeto SQL.
    DATABASES = {
        'default': dj_database_url.config(default='postgres:localhost')   
    }
    
    #  Honra o cabeçalho 'x-Fowarded-Proto' para request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FOWARDED_PROTO', 'https')  # Garante o funcionamento das requisições HTTPS seguras.
    
    # Cabeçalhos para permitir todos os hosts
    ALLOWED_HOSTS = ['*']  # Permite que quaisquer serves atendam as requisições, se debug = False, devemos especificar um host_allowed, como o Heroku.
    
    #  Configuração de recursos estáticos
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Isso aqui cuida de todos os arquivos estáticos, imagens, sons, vídeos, css, js etc...
    STATIC_ROOT = 'staticfiles'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )