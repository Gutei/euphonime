from django.core.mail import send_mail

def send_html_email(username, sender, recipients, subject, content):

    try:
        send_mail(subject, 'EuphoNime', sender, recipients, html_message=content, fail_silently=False)
    except Exception as e:
        return 'Send email to {} Failed'.format(recipients[0])

    return 'Send email to {} Success'.format(recipients[0])