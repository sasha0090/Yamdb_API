from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="review"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review"
    )
    text = models.TextField("Текст")
    score = models.IntegerField(
        "Оценка", validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_review",
            )
        ]

    def __str__(self):
        return self.text[30]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comment"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment"
    )
    text = models.TextField("Текст")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text[30]
