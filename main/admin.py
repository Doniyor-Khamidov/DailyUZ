from django.contrib import admin
from django.utils.html import format_html
from main.models import Category, Tag, Context, Article, Newsletter, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ContextInline(admin.StackedInline):
    model = Context
    extra = 1

class CommentInline(admin.StackedInline):
    model = Context
    extra = 1





@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'intro', 'cover_image', 'reading_time', 'author',
        'published', 'views', 'category', 'created_at', 'important',
    )
    inlines = [ContextInline, CommentInline]

    def cover_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="140" height="80" style="object-fit:cover; border-radius:6px;" />',
                obj.image.url
            )
        return "-"

    cover_image.short_description = 'Cover'

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject','message','phone', 'seen')
    list_editable = ('seen',)

