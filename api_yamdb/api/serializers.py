from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class CustomUserSerializer(serializers.ModelSerializer):
    """Класс для переопределения нового эндпоинта"""

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )

    def validate(self, data):
        if data.get("username") == "me":
            raise serializers.ValidationError("Username указан неверно!")
        return data


class AuthSignUpSerializer(serializers.ModelSerializer):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    class Meta:
        model = User
        fields = ("email", "username")


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    genre = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category"
        )
        model = Title
