from django.shortcuts import render


def get_privacy_policy(request):
    template_name = 'euphonime/_footer_content/privacy_policy.html'
    return render(request, template_name)


def get_disclaimer(request):
    template_name = 'euphonime/_footer_content/disclaimer.html'
    return render(request, template_name)
