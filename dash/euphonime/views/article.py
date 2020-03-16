from django.shortcuts import render
from euphonime.models import Article


def get_article(request, pk):
    template_name = 'euphonime/article.html'
    article = Article.objects.filter(id=pk).first()
    news_article = Article.objects.filter(is_publish=True).order_by('-updated')[:4]
    context = {
        'article': article,
        'news_article': news_article
    }
    return render(request, template_name, context)
