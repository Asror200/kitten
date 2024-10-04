from django.contrib import admin
from django.utils.html import format_html
from cats.models import Cat, Image, Video, Comment, Breed


# Register your models here.

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'breed', 'color', 'date_of_birth', 'user',)
    search_fields = ('name', 'breed',)
    list_filter = ('date_of_birth', 'color', 'user',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat', 'get_image')
    search_fields = ('cat',)
    list_filter = ('cat',)

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<span>No image</span>')

    get_image.short_description = 'Image'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat', 'get_video')
    search_fields = ('cat',)
    list_filter = ('cat',)

    def get_video(self, obj):
        if obj.video:
            return format_html(
                '<video controls class="rounded-circle" style="width: 50px; height: 50px;"> '
                '<source src="{}" type="video/mp4"></video>',
                obj.video.url)
        return format_html('<span>No Video</span>')

    get_video.short_description = 'Video'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat', 'user', 'text',)
    search_fields = ('cat', 'comment', 'user',)
    list_filter = ('cat', 'user',)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)
