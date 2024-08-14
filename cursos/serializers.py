from rest_framework import serializers

from .models import Curso, Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):
  
  # configurações extras das classes
  # dizendo que write_only true,(só ao escrever) o email não 
  # vai ser apresentado quando alguém consultar as avaliacoes
  # apenas no cadastro
  class Meta:
    extra_kwargs = {
      'email': {'write_only': True}
    }
    # indica o model do model serializer
    model = Avaliacao
    # quais campos quero apresentar/mostrar quando o model é solicitado
    fields = {
      'id',
      'curso',
      'nome',
      'email',
      'comentario',
      'criacao',
      'ativo'
    }


class CursoSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Curso
    fields = { 
      'id',
      'titulo',
      'url',
      'criacao',
      'ativo'
    }