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
MEDIA_URL = '/media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```