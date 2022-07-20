from rest_framework.pagination import PageNumberPagination


class ReviewCommentPagination(PageNumberPagination):
    page_size = 10
