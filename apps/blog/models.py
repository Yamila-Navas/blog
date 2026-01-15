from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class publishedManager(models.Manager):
    '''
    Administrador personalizado para posts publicados
    Forma de uso: Post.published.all()
    '''
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)



class Post(models.Model):

    class Status(models.TextChoices):
        '''
        ENTRADAS Y SALIDAS
        Post.Status.choices => [('DF', 'Draft'), ('PB', 'Published')]
        Post.Status.labels  => ['Draft', 'Published']
        Post.Status.values  => ['DF', 'PB']
        Post.Status.names   => ['DRAFT', 'PUBLISHED']
        '''
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    tags = TaggableManager()  # Añade soporte para etiquetas

    objects = models.Manager()  # El administrador por defecto
    published = publishedManager()  # Nuestro administrador personalizado


    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        '''
        Construye la URL para acceder a una entrada específica
        basada en su ID.
        '''
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    

class Comment(models.Model):
    '''
    Clase para gestionar los comentarios de las entradas del blog.
    Cada comentario está asociado a una entrada específica.
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
