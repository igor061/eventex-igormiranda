from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.core.mail import message
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    #context = dict(name='Igor Miranda', CPF='12345678901', email='igor061@gmail.com', phone='61-99999-9999')
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    #Send Mail
    template_name = 'subscriptions/subscription_email.txt'
    context = form.cleaned_data
    subject = 'Confirmação de inscrição'
    from_ = settings.DEFAULT_FROM_EMAIL
    to_ = [from_, form.cleaned_data['email']]
    form.full_clean()

    _send_mail(subject, from_, to_, template_name, context)

    messages.success(request, 'Inscrição realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/')

def new(request):
    context = { 'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


def _send_mail(subject, from_, to_, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, to_)
