from django.contrib import admin

from .models import (
    Book,
    Genere,
    Character,
)


admin.site.register(Character)


@admin.register(Genere)
class GenereAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "name",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",
        "author",
        "publisher",
    )
    search_fields = (
        "id",
        "title",
        "author",
        "publisher",
        "series",
        "language",
        "description",
        "isbn",
    )
    list_filter = ("created",)

    readonly_fields = ["id"]
    list_per_page = 50

    fieldsets = (
        (
            "Book Info",
            {
                "fields": (
                    "id",
                    "title",
                    "author",
                    "description",
                    "publisher",
                    "series",
                    "language",
                    "isbn",
                    "pages",
                    "image",
                ),
            },
        ),
        (
            "Characters and Generes",
            {
                "fields": (
                    "characters",
                    "geners",
                ),
            },
        ),
        (
            "Price and Rating",
            {
                "fields": (
                    "price",
                    "rating",
                ),
            },
        ),
    )
    ordering = ("updated",)
