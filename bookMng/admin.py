from django.contrib import admin
from .models import MainMenu, Book, Rating, Favorite  # add more if you have Comments later

# Optional: control how each model displays in the admin list

@admin.register(MainMenu)
class MainMenuAdmin(admin.ModelAdmin):
    list_display = ('item', 'link')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'username', 'publishdate')
    search_fields = ('name', 'username__username')
    list_filter = ('publishdate',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('book__name', 'user__username')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('book', 'user')
    search_fields = ('book__name', 'user__username')
