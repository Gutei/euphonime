from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from euphonime.models import Anime, Character, AnimeGenre, Quote


def list_quote(request):
    template_name = 'euphonime/quote/list-quote2.html'

    quote = Quote.objects.order_by('-updated')
    paginator = Paginator(quote, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    quote_page = paginator.get_page(page)

    context = {
        'quotes': quote_page,
    }
    return render(request, template_name, context)
