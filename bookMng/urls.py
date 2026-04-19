from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('search', views.search_books, name='search_books'),
    
    # Book management
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('book_edit/<int:book_id>', views.book_edit, name='book_edit'),
    
    # Cart functionality
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>', views.cart_add, name='cart_add'),
    path('cart/remove/<int:book_id>', views.cart_remove, name='cart_remove'),
    path('cart/clear', views.cart_clear, name='cart_clear'),
    path('cart/update/<int:book_id>/<str:action>', views.cart_update_qty, name='cart_update_qty'),
    path('cart/move-to-favorite/<int:book_id>', views.cart_move_to_favorite, name='cart_move_to_favorite'),
    path('checkout', views.checkout, name='checkout'),
    
    # Favorites functionality
    path('fav/toggle/<int:book_id>', views.toggle_favorite, name='toggle_favorite'),
    path('favorites', views.favorite_list, name='favorite_list'),
    path('favorite/move-to-cart/<int:book_id>', views.favorite_move_to_cart, name='favorite_move_to_cart'),
    
    # Rating functionality
    path('book/<int:book_id>/rate/<int:value>', views.rate_book, name='rate_book'),
]
