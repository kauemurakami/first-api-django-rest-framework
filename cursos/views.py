from rest_framework.views import APIView # receber a req 
from rest_framework.response import Response # preparar resposta da req


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