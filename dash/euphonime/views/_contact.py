from django.shortcuts import render


def get_contact(request):
    template_name = 'euphonime/_contact/contact.html'
    return render(request, template_name)
