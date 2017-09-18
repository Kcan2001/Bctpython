from django.contrib import admin

from .models import Post, Category


# Determine what we want to see on Trip Images list page
class CategoryAdmin(admin.ModelAdmin):
    # Will display this fields at Category list page
    list_display = ['title', 'posts_count']

    class Meta:
        model = Category

    # Will count how many posts within a category:
    def posts_count(self, obj):
        query = Category.objects.get(pk=obj.pk)
        return query.posts.count()
    posts_count.short_description = 'Posts Count'

    # Optimization for sql queries
    def get_queryset(self, request):
        return super(CategoryAdmin, self).get_queryset(request).prefetch_related('posts')


# Determine what we want to see at Blog Posts list page
class PostAdmin(admin.ModelAdmin):
    # Hierarchy by created date field
    date_hierarchy = 'created_date'
    # Will order our posts for descending creation date
    ordering = ['-created_date']
    # Search for author and posts title
    search_fields = ['title', 'author']
    # Display this fields at Blog Posts list page
    list_display = ['title', 'author', 'created_date', 'published_date', 'is_draft']
    # Filter by this fields:
    list_filter = ['category', 'is_draft', 'created_date', 'published_date']

    class Meta:
        model = Post

    # Optimization for sql queries
    def get_queryset(self, request):
        return super(PostAdmin, self).get_queryset(request).select_related('author').prefetch_related('category')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
