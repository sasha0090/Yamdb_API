from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action, api_view
from rest_framework import viewsets, status, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from . import serializers
from .pagination import ReviewCommentPagination
from .permissions import (CommentPermission, IsAdmin,
                          IsAdminOrReadonly, ReviewPermission)
from .serializers import (UserSerializer, UserEmailSerializer,
                          TokenSerializer, AdminSerializer,
                          TitleSerializer)


from api_yamdb import settings
from reviews.models import Title, Category, Genre
from users.models import User


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all()
        .annotate(rating=Avg("reviews__score"))
    )
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadonly, ]


class GenreViewSet(viewsets.ModelViewSet):
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [IsAdminOrReadonly, ]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [ReviewPermission]
    pagination_class = ReviewCommentPagination

    def get_queryset(self):
        """Достаем отзывы произведения"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

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


@api_view(["post"],)
def signup(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(User, username=request.data.get("username"))
    if not user.confirmation_code:
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
    send_mail(
        subject="Confirmation code",
        message=f"{user.confirmation_code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(user.email,),
    )
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(["post"])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data.get("username"))

    if default_token_generator.check_token(
        user, serializer.data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [CommentPermission]
    pagination_class = ReviewCommentPagination

    def get_queryset(self):
        """Достаем комментарии к отзыву произведения"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        review = get_object_or_404(
            title.reviews, pk=self.kwargs.get("review_id")
        )
        return review.comments.all()

    def perform_create(self, serializer):
        """Добавляем комментарий к отзыву произведения"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(
            title.reviews, pk=self.kwargs.get("review_id")
        )

        title_data = {"review": review, "author": self.request.user}
        serializer.save(**title_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = "username"
    permission_classes = [
        IsAdmin,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ("username",)
    pagination_class = LimitOffsetPagination

    @action(
        methods=["patch", "get"],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path="me",
        url_name="me",
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        if self.request.method == "PATCH" and user.role != "user":
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)