from django.shortcuts import render

def view(request):
    pass

def help(request):
    return render(request, 'jobs/barline-input-help.html')
