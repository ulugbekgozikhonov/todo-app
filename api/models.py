from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        # Bir user bir xil nomli ikkita kategoriya yarata olmasligi uchun
        unique_together = [["name", "user"]]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Todo(models.Model):
    class PriorityChoices(models.TextChoices):
        LOW = "low", "Low"
        MID = "mid", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MID,
    )
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="todos",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todos",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
