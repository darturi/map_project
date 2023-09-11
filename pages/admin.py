from django.contrib import admin
from .models import Address, Comment


class CommentInLine(admin.TabularInline):
    # The model being used for the comments
    model = Comment
    # The number of extra empty comment slots you will see on the admin page
    extra = 0


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "address",
    ]
    # data on how to display comments related to an article in admin
    inlines = [
        CommentInLine,
    ]


admin.site.register(Address, AddressAdmin)
admin.site.register(Comment)
