from django.core.paginator import Paginator
from django.shortcuts import render
from euphonime.models import Article


def get_article(request, pk):
    template_name = 'euphonime/article/get-article.html'
    article = Article.objects.filter(id=pk).first()
    news_article = Article.objects.filter(is_publish=True).order_by('-updated')[:4]
    context = {
        'article': article,
        'news_article': news_article
    }
    return render(request, template_name, context)


def list_article(request):
    template_name = 'euphonime/article/list-article.html'
    articles = Article.objects.filter(is_publish=True).order_by('-updated')

    paginator = Paginator(articles, 9)  # Show 25 contacts per page
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    context = {
        'articles': articles_page
    }
    return render(request, template_name, context)
