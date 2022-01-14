from django.http import HttpResponse

no_context_int: int = 0

def no_context_view(request):
    global no_context_int
    no_context_int += 1
    return HttpResponse("i=%s" % str(no_context_int))
