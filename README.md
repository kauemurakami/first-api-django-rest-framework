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

##### Criando Models Serializers
Ajuda a codificar nossa classe e seus atributos para json e vice versa.  
Em `escola/cursos/` crie um arquivo chamado `serializers.py`, deve estat no mesmo nível de `models.py` dentro do seu diretório `cursos/`, tendo feito isso, entre no arquivo e vamos criar os serializers pra nossas classes:  
```python
from rest_framework import serializers

from .models import Curso, Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):
  
  class Meta:
    extra_kwargs = {
      'email': {'write_only': True} # só no momento escrita
      #como email e senha por exemplo é um dado sensível, não
      #vamos exibir, apenas no momento de escrever/criar.
    }
    # indica o model do model serializer
    model = Avaliacao
    # quais campos quero apresentar/mostrar quando o model é solicitado
    fields = (
      'id',
      'curso',
      'nome',
      'email',
      'comentario',
      'avaliacao',
      'criacao',
      'ativo'
    )


class CursoSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Curso
    fields = ( 
      'id',
      'titulo',
      'url',
      'criacao',
      'ativo'
    )
``` 
Com isso vamos poder enviar e receber respostas json baseado nos nossos models serializers.  

##### Testando nossos serializers
Primeiro vamos abrir o shell do python, digite em seu terminal `...escola>$ python manage.py shell`  
Você verá seu terminal diferente, algo como  
```shell
Python 3.12.5 (tags/v3.12.5:ff3bc82, Aug  6 2024, 20:45:27) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```  
Significa que esta dentro do shell do python.  
Agora vamos emular uma serialização da nossa classe serializer, neste caso vamos testar apenas a do `Curso`, mas fique a vontade pra fazer o mesmo pra `Avaliacao`, você pode usar `Ctrl + L` para limpar o terminal quadno necessário.  
Agora vamos começar <br/><br/>

Começando pelos imports faça:  
```shell
>>> from rest_framework.renderers import JSONRenderer 
```
Esse será responsável por renderizar nosso serializer em json
Agora vamos importar nosso `model`:
```shell
>>>from cursos.models import Curso
```
E também o import do serializer
```shell
>>>from cursos.serializers import CursoSerializer
```
Caso tudo esteja correndo bem, nenhum erro será exibido e uma nova linha em branco `>>>` aparecerá sempre após um comando correto.<br/><br/>

Continuando agora, vamos buscar o último curso que adicionamos via `django admin`: 
```shell
>>>curso = Curso.objects.latest('id')
```
Agora vamos verificar o que está na variável:
```shell
>>>curso
```
Isso deve retornar u último curso que você adicionou, o resultado será algo como:  
```shell
>>> curso
<Curso: Programação com JavaScript>
```  
Você pode testar também: `>>> curso.titulo`.<br/><br/>

Vamos agora criar nossa variavel serializer:
```shell
>>>serializer = CursoSerializer(curso)
```
Estamos pegando um objeto python, do `models` e passando esse objeto para o `serializers`.
Vamos ver agora o que tem nessa nossa variável `serializer`:  
```shell
>>> serializer
```
Você verá literalmente o nosso model `Curso`
Agora para converter em json basta usar:  
```python
>>> serializer.data
```
Agora você terá seu objeto em formato json.  

##### Criando APIViews
Em `escola/cursos` no arquivo `views.py`, comece removendo todo o conteúdo, em seguida vamos definir nossas requisições, sendo elas `GET` e depois `POST`.  

Definindo as funções `GET` e estrutura inicial:  
```python
from rest_framework.views import APIView # receber a requisição
from rest_framework.response import Response # preparar resposta da requisição


from cursos.models import Curso, Avaliacao
from cursos.serializers import CursoSerializer, AvaliacaoSerializer


class CursoAPIView(APIView):
  """
  Api de cursos
  """
  def get(self, request):
    cursos = Curso.objects.all()
    serializer = CursoSerializer(cursos, many = True) # many -> muitos
    return Response(serializer.data)
  

class AvaliacaoAPIView(APIView):
  """
  Api de avaliacoes
  """
  def get(self, request):
    avaliacoes = Avaliacao.objects.all()
    serializer = AvaliacaoSerializer(avaliacoes, many = True)
    return Response(serializer.data)
```
.<br/>
Agora que definimos as `views`, precisamos criar `rotas` para acessá-las.  
Em `cursos/` crie um novo arquivo chamado `urls.py`, deve estar no mesmo nível de `models.py` e `serializers.py`, e vamos inserir o seguinte conteúdo:  
```python
from django.urls import path

from .views import CursoAPIView, AvaliacaoAPIView

urlpatterns = [
  path('cursos/', CursoAPIView.as_view(), name='cursos'),
  path('avaliacoes/', AvaliacaoAPIView.as_view(), name='avaliacoes')
]
```
Com isso criamos endpoints para nossas `APIViews`.  
Agora vamos informar para o arquivo `urls.py` do projeto (`escola/escola/urls.py`) que temos novos endpoints/rotas.  
Já no arquivo adicione as seguintes linhas:  
```python
urlpatterns = [
    path('api/v1/', include('cursos.urls')), <<<
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls'))
]
```
Agora vá até seu navegador e acesse a url `http://localhost:5000/api/v1/cursos` a lista de cursos aparecerá para você em formato json, procure explorar os botões disponíveis e faça o mesmo para `/avaliacoes`.  
Veremos em formato de api, e você também pode ver em formato json com o dropdown do botão GET.  

##### Implementando funções post a nossas APIViews
No mesmo arquivo `curso/views.py` vamos adicionar nossos endpoint `POST`, para inserir dados, comece adicionando o import de `status` do próprio `drf` para que possamos adicioonar status http em nossas responses.  
```python
from rest_framework.views import APIView # receber a req 
from rest_framework.response import Response # preparar resposta da req
from rest_framework import status # status http <<<<<>>
```
Agora em `CursoAPIView` vamos criar outra função, abaixo da nossa `def get` inicial e adicione a função `POST` responsável por criar um novo curso:  
```python
def post(self, request):
    serializer = CursoSerializer(data=request.data)
    #verificando se os dados são validos
    #caso não lançamosuma exceção e paramos aqui
    serializer.is_valid(raise_exception=True) 
    serializer.save() # salva no banco
    return Response(serializer.data, status=status.HTTP_201_CREATED)
```
Agora em `AvaliacaoAPIView` vamos fazer a mesma coisa: 
```python
  def post(self, request):
    serializer = AvaliacaoSerializer(data=request.data)
    serializer.is_valid()
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
```
Agora você pode usar o `Postman` ou outros programas de clients http para testar, você também pode acessar a url do get, efetuar o login, e aparecerá um campo `content` e do prório navegador fazer a requisição post.  


