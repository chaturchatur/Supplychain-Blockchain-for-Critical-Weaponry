from django.urls import path
from .views import IndentListView,CreateIndentView,IndentView,PartView,RegisterPart,ViewEntity
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/',login_required()(IndentListView.as_view())),
    path('create_indent/',login_required()(CreateIndentView)),
    path('indent/<id>',login_required()(IndentView.as_view())),
    path('part/<slug:pk>',login_required()(PartView.as_view())),
    path('register_part/',login_required()(RegisterPart.as_view())),
    path('entity/<slug:entity_hash>',login_required()(ViewEntity.as_view())),
]