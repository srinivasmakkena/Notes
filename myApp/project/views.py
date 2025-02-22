from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Page, Section

def index(request):
    # Group pages by section
    sections = Section.objects.all()
    grouped_pages = {}
    for obj in Page.objects.all():
        if not obj.section:
            obj.save()
    for section in sections:
        pages = Page.objects.filter(section=section)
        grouped_pages[section] = pages
    return render(request, "index.html", {'grouped_pages': grouped_pages})

def add_page(request):
    if request.method == 'POST':
        page_name = request.POST.get('pageName')
        page_content = request.POST.get('pageContent')
        section_id = request.POST.get('section')

        # Get the selected section or use the default section
        if section_id:
            section = Section.objects.get(id=section_id)
        else:
            section, created = Section.objects.get_or_create(title='')

        page = Page(name=page_name, content=page_content, section=section)
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
        section_id = request.POST.get('section')

        if link_file:
            # Read file content
            file_content = link_file.read().decode('utf-8')

            # Get the selected section or use the default section
            if section_id:
                section = Section.objects.get(id=section_id)
            else:
                section, created = Section.objects.get_or_create(title='')

            # Create a new Page object
            page = Page(name=link_name, content=file_content, section=section)
            page.save()

            messages.success(request, 'File added successfully!')
            return redirect('home')
        messages.error(request, 'No file uploaded.')
        return redirect('home')

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def edit_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)

    if request.method == 'POST':
        page.name = request.POST.get('pageName')
        page.content = request.POST.get('pageContent')
        section_id = request.POST.get('section')
        if section_id:
            page.section = Section.objects.get(id=section_id)
        page.save()
        messages.success(request, 'Page updated successfully!')
        return redirect('pageview', id=page.id)

    sections = Section.objects.all()
    return render(request, 'edit_page.html', {'page': page, 'sections': sections})

def delete_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Page deleted successfully!')
    return redirect('home')


def rename_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        new_title = request.POST.get('newTitle')
        section.title = new_title
        section.save()
        messages.success(request, 'Section renamed successfully!')
    return redirect('home')

def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        section.delete()
        messages.success(request, 'Section deleted successfully!')
    return redirect('home')

@csrf_exempt
def update_page_section(request):
    if request.method == 'POST':
        page_id = request.POST.get('page_id')
        new_section_id = request.POST.get('new_section_id')

        try:
            page = Page.objects.get(id=page_id)
            new_section = Section.objects.get(id=new_section_id)
            page.section = new_section
            page.save()
            return JsonResponse({'success': True})
        except (Page.DoesNotExist, Section.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid page or section ID.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def create_section(request):
    if request.method == 'POST':
        section_title = request.POST.get('sectionTitle')
        section, created = Section.objects.get_or_create(title=section_title)
        if created:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Section already exists.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})