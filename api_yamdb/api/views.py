from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action, api_view
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .pagination import ReviewCommentPagination
from .permissions import (IsAuthorOrStaffOrReadOnly, IsAdminOrStaffPermission,
                          IsUserForSelfPermission)
from .serializers import (AuthSignUpSerializer, AuthTokenSerializer,
                          UserSerializer)

from .utils import generate_and_send_confirmation_code_to_email

from review.models import Title
from users.models import User


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all()
        .annotate(rating=Avg("reviews__score"))
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthorOrStaffOrReadOnly]
    pagination_class = ReviewCommentPagination

    def get_queryset(self):
        """Достаем отзывы произведения"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.review.all()

    def perform_create(self, serializer):
        """Добавляем отзыв к произведению и назначаем автора"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        title_data = {"title": title, "author": self.request.user}
        try:
            serializer.save(**title_data)
        except IntegrityError:
            raise ValidationError(
                "The fields title, following must make a unique set."
            )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorOrStaffOrReadOnly]
    pagination_class = ReviewCommentPagination

    def get_queryset(self):
        """Достаем комментарии к отзыву произведения"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        review = get_object_or_404(
            title.review, pk=self.kwargs.get("review_id")
        )
        return review.comment.all()

    def perform_create(self, serializer):
        """Добавляем комментарий к отзыву произведения"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(
            title.review, pk=self.kwargs.get("review_id")
        )

        title_data = {"review": review, "author": self.request.user}
        serializer.save(**title_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrStaffPermission,)
    search_fields = ("=username",)
    lookup_field = "username"

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(IsUserForSelfPermission,),
    )
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        partial=True
                                        )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def signup_new_user(request):
    username = request.data.get("username")
    if not User.objects.filter(username=username).exists():
        serializer = AuthSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["username"] != "me":
            serializer.save()
            generate_and_send_confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Username указан невено!",
                        status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    serializer = AuthSignUpSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data["email"] == user.email:
        serializer.save()
        generate_and_send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("Почта указана неверно!",
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Пользователь не найден",
                        status=status.HTTP_404_NOT_FOUND)
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token_data = {"token": str(refresh.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response("Код подтверждения неверный",
                    status=status.HTTP_400_BAD_REQUEST)
