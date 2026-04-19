from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Favorite
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Rating
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.urls import reverse


def index(request):
    """Enhanced homepage with featured book and bestsellers"""
    books = Book.objects.all().order_by('-publishdate')
    featured = books.first() if books else None
    bestsellers = books[:8]
    
    return render(request, 'bookMng/index.html', {
        'item_list': MainMenu.objects.all(),
        'featured': featured,
        'bestsellers': bestsellers,
    })


@login_required(login_url='login')
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.username = request.user
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'bookMng/postbook.html', {
        'form': form,
        'item_list': MainMenu.objects.all(),
        'submitted': submitted
    })


def displaybooks(request):
    # Start with all books
    books = Book.objects.all().order_by("-publishdate")

    # Read selected category from ?category=
    selected_category = request.GET.get("category", "all")

    # Filter by category if not "all"
    if selected_category != "all":
        books = books.filter(category=selected_category)

    # Compute rating / favorite flags
    for b in books:
        b.avg_rating = b.ratings.aggregate(Avg('value'))['value__avg'] or 0
        b.avg_rating = round(b.avg_rating, 2)
        b.total_ratings = b.ratings.count()
        b.star_fill = int((b.avg_rating / 5) * 100)
        b.is_favorite = (
            request.user.is_authenticated
            and Favorite.objects.filter(book=b, user=request.user).exists()
        )

    context = {
        "item_list": MainMenu.objects.all(),
        "book_list": books,              # used by some templates
        "books": books,                  # used by others (safety)
        "categories": Book.CATEGORY_CHOICES,
        "selected_category": selected_category,
    }

    return render(request, "bookMng/displaybooks.html", context)

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    avg_rating = book.ratings.aggregate(Avg('value'))['value__avg'] or 0
    avg_rating = round(avg_rating, 2)
    total_ratings = book.ratings.count()
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(book=book, user=request.user).exists()
    star_fill = int((avg_rating / 5) * 100)
    
    user_rating = 0
    if request.user.is_authenticated:
        existing = Rating.objects.filter(book=book, user=request.user).first()
        if existing:
            user_rating = existing.value

    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'avg_rating': avg_rating,
        'total_ratings': total_ratings,
        'is_favorite': is_favorite,
        'user_rating': user_rating,
        'star_fill': star_fill,
    })


@login_required(login_url='login')
def mybooks(request):
    books = Book.objects.filter(username=request.user).order_by('-publishdate')
    return render(request, 'bookMng/mybooks.html', {
        'books': books,
        'item_list': MainMenu.objects.all()
    })


@login_required(login_url='login')
def book_delete(request, book_id):
    """Enhanced delete with permission checks"""
    book = get_object_or_404(Book, id=book_id)

    # Only allow admin (superuser) or the owner of the book
    if not (request.user.is_superuser or book.username == request.user):
        return HttpResponseForbidden("You are not allowed to delete this book.")

    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully.")
        
        # Admin goes back to all books, user goes to their books
        if request.user.is_superuser:
            return redirect("displaybooks")
        else:
            return redirect("mybooks")

    return render(request, 'bookMng/book_delete.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
    })


@login_required(login_url='login')
def book_edit(request, book_id):
    """Edit book functionality"""
    book = get_object_or_404(Book, id=book_id, username=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {book.name}")
            return redirect('mybooks')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookMng/book_edit.html', {
        'form': form,
        'book': book,
        'item_list': MainMenu.objects.all()
    })


def aboutus(request):
    return render(request, "bookMng/aboutus.html", {
        "item_list": MainMenu.objects.all()
    })


def search_books(request):
    """Enhanced search with category support"""
    q = (request.GET.get("q") or "").strip()
    results = Book.objects.none()
    
    if q:
        normalized = q.lower()
        # Fix hyphen mismatch for Non-fiction
        if normalized == "non-fiction":
            normalized = "nonfiction"
        
        results = Book.objects.filter(
            Q(name__icontains=q) |
            Q(web__icontains=q) |
            Q(category__iexact=normalized)
        )
        
        for b in results:
            b.avg_rating = b.ratings.aggregate(Avg('value'))['value__avg'] or 0
            b.avg_rating = round(b.avg_rating, 2)
    
    return render(request, "bookMng/search.html", {
        "q": q,
        "results": results,
        "item_list": MainMenu.objects.all(),
    })


# ============ CART FUNCTIONALITY ============
CART_KEY = "cart"

def _get_cart(session):
    cart = session.get(CART_KEY, {})
    session[CART_KEY] = cart
    return cart


def cart_add(request, book_id):
    """Enhanced cart add with quantity and smart redirect"""
    book = get_object_or_404(Book, id=book_id)
    cart = _get_cart(request.session)
    
    # Get quantity (POST or default)
    if request.method == "POST":
        try:
            qty = int(request.POST.get("qty", 1))
        except ValueError:
            qty = 1
    else:
        qty = 1
    
    if qty < 1:
        qty = 1
    
    cart[str(book.id)] = cart.get(str(book.id), 0) + qty
    request.session.modified = True
    messages.success(request, f"{qty} × '{book.name}' added to cart!")
    
    # Return to previous page or cart
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    else:
        return redirect("cart_detail")


def cart_remove(request, book_id):
    cart = _get_cart(request.session)
    cart.pop(str(book_id), None)
    request.session.modified = True
    return redirect('cart_detail')


def cart_clear(request):
    request.session[CART_KEY] = {}
    request.session.modified = True
    return redirect('cart_detail')


def cart_update_qty(request, book_id, action):
    """Update cart item quantity"""
    cart = _get_cart(request.session)
    key = str(book_id)
    if key in cart:
        if action == 'increase':
            cart[key] += 1
        elif action == 'decrease':
            cart[key] = max(1, cart[key] - 1)
    request.session.modified = True
    return redirect('cart_detail')


def cart_detail(request):
    """Enhanced cart with favorite suggestions"""
    cart = _get_cart(request.session)
    items = []
    total = 0
    
    for sid, qty in cart.items():
        b = Book.objects.get(id=int(sid))
        line_total = b.price * qty
        total += line_total
        items.append({"book": b, "qty": qty, "line_total": line_total})

    # Get favorites if user is authenticated
    favorite_books = []
    if request.user.is_authenticated:
        favorite_books = Book.objects.filter(favorites__user=request.user).exclude(
            id__in=[int(sid) for sid in cart.keys()]
        )[:4]

    return render(request, "bookMng/cart.html", {
        "items": items,
        "total": total,
        "favorite_books": favorite_books,
        "item_list": MainMenu.objects.all()
    })


@login_required(login_url='login')
def cart_move_to_favorite(request, book_id):
    """Move cart item to favorites"""
    book = get_object_or_404(Book, id=book_id)
    Favorite.objects.get_or_create(book=book, user=request.user)
    cart = _get_cart(request.session)
    cart.pop(str(book_id), None)
    request.session.modified = True
    messages.success(request, f"Moved {book.name} to favorites")
    return redirect('cart_detail')


@login_required(login_url='login')
def favorite_move_to_cart(request, book_id):
    """Move favorite to cart"""
    cart = _get_cart(request.session)
    cart[str(book_id)] = cart.get(str(book_id), 0) + 1
    request.session.modified = True
    messages.success(request, "Added to cart")
    return redirect('cart_detail')


@login_required(login_url='login')
def checkout(request):
    """Checkout functionality"""
    cart = _get_cart(request.session)
    items = []
    total = 0
    
    for sid, qty in cart.items():
        b = Book.objects.get(id=int(sid))
        line_total = b.price * qty
        total += line_total
        items.append({"book": b, "qty": qty, "line_total": line_total})

    if request.method == 'POST':
        request.session[CART_KEY] = {}
        request.session.modified = True
        messages.success(request, "Order placed successfully!")
        return redirect('index')

    return render(request, "bookMng/checkout.html", {
        "items": items,
        "total": total,
        "item_list": MainMenu.objects.all()
    })


# ============ FAVORITES FUNCTIONALITY ============
@login_required(login_url='login')
def toggle_favorite(request, book_id):
    """Toggle favorite status with AJAX support"""
    book = get_object_or_404(Book, id=book_id)
    fav, created = Favorite.objects.get_or_create(book=book, user=request.user)
    
    if not created:
        fav.delete()
        is_favorite = False
    else:
        is_favorite = True

    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})

    return redirect('book_detail', book_id)


@login_required(login_url='login')
def favorite_list(request):
    """List user's favorite books"""
    books = Book.objects.filter(favorites__user=request.user)
    return render(request, 'bookMng/favorites.html', {
        'books': books,
        'item_list': MainMenu.objects.all()
    })


# ============ RATING FUNCTIONALITY ============
@login_required(login_url='login')
def rate_book(request, book_id, value):
    """Rate a book"""
    book = get_object_or_404(Book, id=book_id)
    value = max(1, min(5, int(value)))
    Rating.objects.update_or_create(
        book=book, user=request.user, defaults={"value": value}
    )
    return redirect('book_detail', book_id=book.id)


# ============ AUTH FUNCTIONALITY ============
def logout_then_home(request):
    logout(request)
    return redirect("index")
