from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from . import serializers
from .pagination import ReviewCommentPagination
from .permissions import IsAuthorOrReadOnly, IsStaff
from review.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly | IsStaff]
    pagination_class = ReviewCommentPagination

    def get_queryset(self):
        """Достаем отзывы произведения"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.review.all()

    def perform_create(self, serializer):
        """Добавляем отзыв к произведению и назначаем автора"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        title_data = {"title": title, "author": self.request.user}
        serializer.save(**title_data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorOrReadOnly | IsStaff]
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
        try:
            serializer.save(**title_data)
        except IntegrityError:
            raise ValidationError(
                "The fields title, following must make a unique set."
            )
