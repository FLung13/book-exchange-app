from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-fiction'),
        ('children', "Children's Books"),
        ('classic', 'Classics'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='book_images/', blank=True, null=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
    )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    book = models.ForeignKey('Book', related_name="favorites", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)

    class Meta:
        unique_together = [("book", "user")]

    def __str__(self):
        return f"{self.user.username} → {self.book.name}"


class Rating(models.Model):
    book = models.ForeignKey('Book', related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("book", "user")]

    def __str__(self):
        return f"{self.book.name} - {self.user.username} ({self.value})"
