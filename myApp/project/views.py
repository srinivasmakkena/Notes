from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Page 
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(request):
    pages_list = Page.objects.all()
    return render(request, "index.html", {'pages': pages_list})

def add_page(request):
    if request.method == 'POST':
        page_name = request.POST.get('pageName')
        page_content = request.POST.get('pageContent')
        page = Page(name=page_name, content=page_content)
        page.save()
        messages.success(request, 'Page added successfully!')
    return redirect('home')

def page_view(request, id):
    page = get_object_or_404(Page, id=id)
    return render(request, 'page_view.html', {'page': page})

@csrf_exempt
def add_file(request):
    if request.method == 'POST':
        link_name = request.POST.get('linkName')
        link_file = request.FILES.get('linkFile')

        if link_file:
            # Read file content
            file_content = link_file.read().decode('utf-8')
            
            # Create a new Page object
            page = Page(name=link_name, content=file_content)
            page.save()

            messages.success(request, 'File added successfully!')
            return redirect('home')
        messages.error(request, 'No file uploaded.')
        return redirect('home')

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
