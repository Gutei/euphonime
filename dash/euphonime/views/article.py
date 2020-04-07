from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from euphonime.models import Article, MetaPage


def get_article(request, pk, slug):
    template_name = 'euphonime/article/get-article.html'
    article = Article.objects.filter(prefix_id=pk, slug=slug).first()
    news_article = Article.objects.filter(is_publish=True).order_by('-updated')[:4]
    meta = MetaPage.objects.filter(page=MetaPage.ARTICLE).exclude(meta_name__in=['title', 'description', 'og:image', 'og:title', 'og:description', 'keywords'])
    context = {
        'article': article,
        'news_article': news_article,
        'meta': meta,
    }
    return render(request, template_name, context)


def list_article(request):
    template_name = 'euphonime/article/list-article.html'
    articles = Article.objects.filter(is_publish=True).order_by('-updated')
    meta = MetaPage.objects.filter(page=MetaPage.ARTICLE)

    search = request.GET.get('search')
    if request.method == 'GET' and search:
        # Q(name__icontains=query) | Q(state__icontains=query)
        articles = Article.objects.filter(Q(title__icontains=search)).order_by('-updated')

    paginator = Paginator(articles, 9)  # Show 25 contacts per page
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    context = {
        'articles': articles_page,
        'meta': meta
    }
    return render(request, template_name, context)
