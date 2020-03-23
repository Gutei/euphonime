from django.shortcuts import render


def get_sitemaps(request):
    template_name = 'sitemaps/sitemap.xml'
    return render(request, template_name, content_type="text/xml")