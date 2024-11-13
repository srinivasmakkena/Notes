from django.urls import path

from . import views
urlpatterns=[
        path('',views.index,name= "home"),
        path('add_page/', views.add_page, name='add_page'),
        path('page/<int:id>/', views.page_view, name='pageview'),
        path('add-file/', views.add_file, name='add_file'),
        path('page_edit/<int:page_id>/edit/', views.edit_page, name='edit_page'),
]
