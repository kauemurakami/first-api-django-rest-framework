### Get Start with django rest

##### Crie um diretório vazio
`/escola`

##### no terminal
Vamos instalar a ultima versão (com LTS) do django project, atualmente está:  
`.../escola>$: pip install django==4.2.15`  
Sempre dar preferencias para versões, não mais atuais, mas sim as que possuem LTS, que significa que vai ter uma manutenção e continuidade maior, isso é bom para aplicações de produção.  
Mesmo a versão atual, hoje 08/08/24 sendo as 5.1.x vamos usar as ultima release com LTS que é a 4.2.15

##### Criando projeto django
`.../escola>$: django-admin startproject escola .`  
O ponto indica que não é preciso criar um subdiretório  
Além de gerar arquivos de configurações necessários para o funcionamento de uma api.  

##### Criando aplicação django
`.../escola>$: django-admin startapp <name_application>`
Isso nos gera uma aplicação, no caso `/cursos` que vem com arquivos de configuração de models, tests, views e uma pasta `/migrations` para nossas migrações para o bd.  

##### Iniciando configurações do projeto
Aqui não focaremos no front ends, apenas na API.  
No diretório gerado com `startproject` que nos gerou os diretório interno `/escola` com os arquivos de configuração.  
Em *settings.py*, procue por um array chamado `INSTALLED_APPS = [...]`, ao fim do conteúdo dele, adicione nossa aplicação `cursos` criada com `startapp`, o código ficará assim: 
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cursos'  
]
```
Altere também `LANGUAGE_CODE` e `TIMEZONE` para : 
```python
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
```
Ao fim do arquivo, abaixo de `STATIC_URL` crie uma novas variaveis chamadas `STATIC_ROOT MEDIA_URL MEDIA_ROOT` com o seguinte conteúdo: 
```python
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

##### Criando models da aplicação
Em `escola/cursos` abra o arquivo `models.py` em seguida adiicone nossas classes, sendo `Base` uma classe `abstract`: 
```python
from django.db import models

class Base(models.Model):
  criacao = models.DateTimeField(auto_now_add=True) 
  atualizacao = models.DateTimeField(auto_now_add=True)
  ativo = models.BooleanField(default=True)

  class Meta:
    abstract = True

class Curso(Base):
  titulo = models.CharField(max_length=255)
  url = models.URLField(unique=True) #não criar dois cursos com mesma url

  class Meta:
    verbose_name = 'Curso'
    verbose_name_plural = 'Cursos'
  
  def __str__(self):
    return self.titulo

class Avaliacao(Base):
  curso = models.ForeignKey(Curso, related_name='avaliacoes', on_delete= models.CASCADE)
  nome = models.CharField(max_length= 255)
  email = models.EmailField()
  comentario = models.TextField(blank=True, default='')
  avaliacao = models.DecimalField(max_digits=2, decimal_places=1)

  class Meta:
    verbose_name = 'Avaliacao'
    verbose_name_plural = 'Avaliacoes'
    unique_together = ['email', 'curso']

  def __str__(self):
    return f'{self.nome} avaliou o curso {self.curso} com nota {self.avaliacao}'
```
Agora Vamos registrar esse `model` no `admin`, em `escola/cursos` abra o arquivo `admin.py` e registre nossos models da seguinte forma :
```python
from django.contrib import admin

# Register your models here.
from .models import Curso, Avaliacao


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
  list_display = ( 'titulo', 'url', 'criacao', 'atualizacao', 'ativo')

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
  list_display = ( 'curso', 'nome', 'email', 'avaliacao', 'criacao', 'atualizacao', 'ativo')
```  
Temos nossos `models` criados e registrados no `admin`, agora podemos rodar nossa `migration`.  
Vamos rodar o seguinte comando a nível de projeto:  
`.../escola>$: python manage.py makemigrations` após isso, caso de tudo certo, algo como :  
```sheel
Migrations for 'cursos':
  cursos\migrations\0001_initial.py
    - Create model Curso
    - Create model Avaliacao
```
deve aparecer para você, caso contrário revise seu `admin` e seus `models` e tente novamente.  
Caso tudo tenha ocorrido bem e recebido um resultado ok no terminal, você pode verirficar em `escola/cursos/migrations` deve ter um titulo como `0001_initial.py`,agora com as `migrations` criadas, vamos agora migrar de fato com:  
`.../escola>$: python manage.py migrate`  
Após isso algo como :
```shell
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, cursos, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```
deve ser exibido no seu terminal.<br/><br/>

##### Criando super user
Agora vamos aproveitar apara criar nosso super usuário:  
`.../escola>$: python manage.py createsuperuser` e preencha os campos que serão pedidos ( usuário, email e senha).  

Com isso agora vamos rodar o servidor:  
`.../escola>$: python manage.py runserver`<br/><br/>

Em caso de erro ao rodar o servidor, basta definir uma porta em `escola/escola/settings.py`: 
```python
...
from django.core.management.commands.runserver import Command as rs
rs.default_port='5000' 

import os
from pathlib import Path
...
```
Adicione esta linha `from django.core.management.commands.runserver import Command as rs rs.default_port='5000'` com a porta de sua preferência e rode novamente o comando `.../escola>$: python manage.py runserver`  

##### Criando objetos via admin
Vá até seu navegador e digite `localhost:5000/admin` caso não tenha definido uma porta, a porta padrão geralmente é `8000`, mas ao rodar `runserver` exibirá a url local da api.  
Va na seção `cursos` e adicione alguns cursos, eu adicionei 3.  
Após isso vá para a seção `avaliacao`, avalie cada um dos cursos, pode ser com um mesmo usuário ou diferentes, lembrando que você pode testar, que ele não receba outra avaliação do mesmo email que já avaliou o mesmo curso.  

##### Criando API
Por enquanto temos apenas o projeto django, sem nenhuma api, vamos então instalar os requisitos para começar.  
##### Instalação e configuração do django-rest-framework
Comece instalando o `django rest framework` com o seguinte comando:  
`.../escola>$:pip install djangorestframework markdown django-filter` 
O `markdown` é utilizado pelo `django rest framework` para criar páginas de documentação da nossa API.  
O `django-filter` facilita a utilização de filtros.<br/><br/>

Vamos aproveitar e criar nossos requirements com:  
`pip freeze > requirements.txt`  
Caso tudo ocorra bem um arquivo `requirements.txt` será criado na raiz do projeto.<br/><br/>

###### Configurando
Em `escola/escola/settings.py` Altere esses trechos de código:  
```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters', <
    'rest_framework', <

    'cursos'
]
```
Agora ao fim do arquivo vamos adicionar : 
```python
#DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
  ),
  'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
  )
}
```
Agora no mesmo diretório em `urls.py` faça a seguinte alteração:  
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls'))
]
```
Estamos adicionando as rotas do django rest framework.  

Agora navegue até a url de login no seu navegador: `http://localhost:5000/api-auth/login/` e verá uma tela criada.
