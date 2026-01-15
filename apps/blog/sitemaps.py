from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    '''
    Este sitemap genera las URLs para las entradas publicadas del blog.
    Proporciona la frecuencia de cambio y la prioridad para los motores de búsqueda.
    Se utiliza para mejorar la indexación de las entradas del blog.
    '''
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.published.all()
    def lastmod(self, obj):
        return obj.updated