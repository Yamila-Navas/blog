from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''
    prepopulated_fields => autocompletado con el campo titulo
    raw_id_fields => por ID en vez de nombre
    date_hierarchy => filtrar por fecha de publicacion
    ordering => oredenar primero por status luego por publish
    '''
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''
    Administrador para los comentarios de las entradas del blog.
    '''
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        '''
        Acción personalizada para aprobar comentarios seleccionados.
        Es decir, establecer su campo 'active' a True segun las condiciones que necesite.
        '''
        queryset.update(active=True)

