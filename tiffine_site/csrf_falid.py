from django.shortcuts import render


def csrf_failure(request, reason=""):
    ctx = {'message': 'There is something wrong with your request !'}
    template = 'csrf.html'
    return render(request, template, ctx)

