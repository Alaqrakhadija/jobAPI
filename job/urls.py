from django.urls import path, include
from job.views import UserViewSet, create_cover_letter, CompanyPositionViewSet

company_list = UserViewSet.as_view({
    'get': 'list',

})
# user_create = UserViewSet.as_view({
#     'post': 'create',
#
# })
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
})
position_list = CompanyPositionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
position_detail = CompanyPositionViewSet.as_view({
    'get': 'retrieve',
})
urlpatterns = [
    path('company/', company_list, name='company-list'),
    # path('users/', user_create, name='user-create'),
    path('company/<int:pk>/', user_detail, name='company-detail'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('company/<int:pk>/positions/', position_list, name='position-list'),
    path('company/<int:pk>/positions/<int:pk2>', position_detail, name='position_detail'),
    path('generate_cover_letter', create_cover_letter, name='create_letter'),
]
