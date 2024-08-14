from rest_framework.views import APIView # receber a req 
from rest_framework.response import Response # preparar resposta da req
from rest_framework import status # status http


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
  
  def post(self, request):
    serializer = CursoSerializer(data=request.data)
    #verificando se os dados são validos
    #caso não lançamosuma exceção e paramos aqui
    serializer.is_valid(raise_exception=True) 
    serializer.save() # salva no banco
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class AvaliacaoAPIView(APIView):
  """
  Api de avaliacoes
  """
  def get(self, request):
    avaliacoes = Avaliacao.objects.all()
    serializer = AvaliacaoSerializer(avaliacoes, many = True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = AvaliacaoSerializer(data=request.data)
    serializer.is_valid()
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)