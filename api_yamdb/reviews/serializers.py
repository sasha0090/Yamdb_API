# from django.shortcuts import get_object_or_404

from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Genre, Title  # , Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'  # ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'  # ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'  # ('id', 'name', 'year', 'description', 'genre', )
        #  'rating', 'description', 'genre', )
        model = Title
