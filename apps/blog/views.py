from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity


from taggit.models import Tag
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm



def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    search_form = SearchForm()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # Paginacion de las entradas del blog, 5 por página:
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {
        'posts': posts,
        'tag': tag,
        'form': search_form
    })
    


def post_detail(request, slug, year, month, day):
    '''
    1- Detalla una entrada del blog específica.
    2- Muestra los comentarios activos para esa entrada.
    3- Proporciona un formulario para añadir nuevos comentarios.
    4- Muestra entradas similares basadas en etiquetas compartidas:
        - Lista hasta 4 posts publicados, distintos al actual,
          que compartan tags con él, ordenados por cuántas tags comparten
          y qué tan nuevos son.
    5- Maneja errores 404 si la entrada no existe.
    6- Renderiza la plantilla 'blog/post/detail.html' con el contexto adecuado: 
        - post
        - comments
        - form
        - similar_posts
    '''
    post = get_object_or_404(
        Post, 
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})


def post_share(request, post_id):
    '''
    Enviar una entrada del blog por correo electrónico.
    '''
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Aquí se enviaría el correo electrónico:
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            subject = (
            f"{cd['name']} ({cd['email']}) "
            f"recommends you read {post.title}"
            )

            message = (
            f"Read {post.title} at {post_url}\n\n"
            f"{cd['name']}\'s comments: {cd['comments']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    '''
    permite añadir un comentario a una entrada del blog
    el formulario lo carga la vista post_detail previamente
    y se envía a esta vista mediante POST
    '''
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/post/comment.html', {
        'post': post,
        'form': form,
        'comment': comment
    })


def post_search(request):
    '''
    Buscar entradas del blog que coincidan con una consulta dada.
    Utiliza SearchVector para buscar en los campos 'title' y 'body'.
    Renderiza la plantilla 'blog/post/search.html' con el formulario de búsqueda,
    la consulta y los resultados encontrados.

    Usando vector, query y rank de búsqueda:
    form : Crea el formulario de búsqueda.
    query : Toma lo que escribió el usuario en el buscador.
    SearchVector : Prepara el texto para buscar por título y cuerpo.
    SearchQuery : Convierte lo que escribió el usuario en algo que PostgreSQL entiende como búsqueda “tipo Google”.
    SearchRank : Calcula qué tan bien coincide cada post con lo buscado.
    filter(rank__gte=0.3) : Descarta resultados flojos. Solo deja los que realmente valen la pena.
    order_by('-rank') : Muestra primero los posts más relevantes.

    Usando TrigramSimilarity para mejorar la búsqueda:
    TrigramSimilarity : Calcula la similitud entre la consulta y los campos 'title' y 'body' usando trigramas.
    filter(similarity__gt=0.1) : Filtra los resultados para incluir solo aquellos con una similitud mayor a 0.1.
    order_by('similarity') : Ordena los resultados por similitud en orden ascendente.

    '''
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # Usando vector, query y rank de búsqueda:
            #search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            #search_query = SearchQuery(query, search_type='websearch', config='english')
            #results = Post.published.annotate(rank =SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')

            # Usando TrigramSimilarity para mejorar la búsqueda
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query) + TrigramSimilarity('body', query)
            ).filter(similarity__gt=0.1).order_by('similarity')

    return render(request, 'blog/post/search.html', {
        'form': form,
        'query': query,
        'results': results
    })