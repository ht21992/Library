from django.shortcuts import render, HttpResponse
from book.models import Book, Genere, Character
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


def main(request):
    try:
        books = Book.objects.all()
        recommendedBook = (
            books.filter(language="English").filter(rating__gt=4.5).order_by("?")[0]
        )
        bannerBooks = books.filter(language="English").order_by("?")[:5]
        featuredBooks = books.filter(rating__gt=4.0).order_by("?")[:4]
        booksPaginator = Paginator(
            books,
            12,
        )
        books = booksPaginator.page(1)
    except IndexError:
        return render(
        request,
        "frontend/main.html",)
    return render(
        request,
        "frontend/main.html",
        context={
            "bannerBooks": bannerBooks,
            "featuredBooks": featuredBooks,
            "books": books,
            "recommendedBook": recommendedBook,
        },
    )


@require_http_methods(["GET"])
def get_objects_partials(request):
    type = request.GET.get("type", "")
    if not type:
        return HttpResponse("view type is not specified")
    searchFilter = request.GET.get("searchFilter", "")
    genreFilter = request.GET.get("genreFilter", "")

    bookPage = request.GET.get("bookPage", 1)
    queryset = Book.objects.all()
    if genreFilter:
        if Genere.objects.filter(name=genreFilter).exists():
            current_Genere = Genere.objects.get(name=genreFilter)
            queryset = queryset.filter(geners=current_Genere)

    if searchFilter:
        queryset = queryset.filter(
            Q(title__icontains=searchFilter)
            | Q(geners__name__icontains=searchFilter)
            | Q(characters__name__icontains=searchFilter)
            | Q(author__icontains=searchFilter)
        ).distinct()


    booksPaginator = Paginator(
        queryset,
        12,
    )

    books = booksPaginator.page(bookPage)
    context = {"books": books, "genreFilter": genreFilter, "searchFilter": searchFilter}
    return render(
        request,
        f"frontend/partials/books_partial.html",
        context=context,
    )
