from django.conf import settings
from django.core import mail
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    #context = dict(name='Igor Miranda', CPF='12345678901', email='igor061@gmail.com', phone='61-99999-9999')

    form = SubscriptionForm(request.POST)

    form.full_clean()

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    #Send Mail
    from_ = settings.DEFAULT_FROM_EMAIL
    to_ = [from_, subscription.email]
    _send_mail(
        'Confirmação de inscrição',
        from_,
        to_,
        'subscriptions/subscription_email.txt',
        {'subscription': subscription},
    )

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))

def new(request):
    context = { 'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)

def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request,
                  'subscriptions/subscription_detail.html',
                  {'subscription': subscription})



def _send_mail(subject, from_, to_, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, to_)
