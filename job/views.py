from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters import rest_framework
from job.chatgpt import generate_response
from job.filters import PositionFilter
from job.models import Position, User, Type
from job.permissions import IsCompanyOrReadOnly, IsOwnerOrReadOnly

from job.serialize import PositionSerializer, UserSerializer


class CompanyPositionViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = PositionSerializer
    filter_backends = [filters.SearchFilter, rest_framework.DjangoFilterBackend]
    search_fields = ['title']
    filterset_class = PositionFilter
    permission_classes = [permissions.IsAuthenticated,
                          IsCompanyOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        company_id = self.kwargs['pk']
        queryset = Position.objects.filter(company__id=company_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

    def retrieve(self, request, pk=None, pk2=None):
        position = get_object_or_404(Position, id=pk2, company_id=pk)
        serializer = self.serializer_class(position)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(type=Type.COMPANY)
        return queryset


@api_view(['POST'])
def create_cover_letter(request):
    if request.method == 'POST':
        user_message = f"write a cover letter for a " \
                       f"{request.data['position']} position with a skills:" \
                       f" {request.data['skills']} and company name:{request.data['name']} "
        response = generate_response(user_message)
        return Response({'response': response})

#
# class CompanyPositionDetail(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     serializer_class = PositionSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def retrieve(self, request, pk=None, pk2=None):
#         position = get_object_or_404(Position, id=pk2, company_id=pk)
#         serializer = self.serializer_class(position)
#         return Response(serializer.data)
