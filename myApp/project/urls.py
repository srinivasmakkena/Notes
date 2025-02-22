from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('add_page/', views.add_page, name='add_page'),
    path('page/<int:id>/', views.page_view, name='pageview'),
    path('add-file/', views.add_file, name='add_file'),
    path('page_edit/<int:page_id>/edit/', views.edit_page, name='edit_page'),
    path('delete_page/<int:page_id>/', views.delete_page, name='delete_page'),
    path('create_section/', views.create_section, name='create_section'),
    path('rename_section/<int:section_id>/', views.rename_section, name='rename_section'),
    path('delete_section/<int:section_id>/', views.delete_section, name='delete_section'),
    path('update_page_section/', views.update_page_section, name='update_page_section'),
]