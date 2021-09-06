from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from profiles_api import serializers, models, permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, IsAuthenticated


class HelloApiView(APIView):


    '''Api View de prueba'''

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        '''Retornar listas  de caracteristicas del APIView'''

        an_api_view = [
            'Usamos metodos HTTP como funciones (get, post, patch, put, delete)',
            'Es similar a una vista tradicional de Django',
            'Nos da el mayor control sobre la logica del nuestra aplicacion',
            'Esta mapeado manualmente a los URLs',
        ]

        return Response({'message': 'Hello', 'an_api_view': an_api_view})

    def post(self, request):
        '''Crea un mensaje con nuestro nombre'''

        serializers = self.serializer_class(data=request.data)

        if serializers.is_valid():
            name = serializers.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializers.errors, status=status.HTTP_404_BAD_REQUEST)
    
    

    def put(self, request, pk=None):
        ''' Maneja actualizar un objeto '''
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        ''' Maneja actualizacion parcial de un objeto '''
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        ''' Borrar un objeto '''
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    '''TEST Api ViewSet'''
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        ''' Para retornar un mensaje de HelloWorld'''

        a_viewset = [
            'Usa acciones (list, create, retrieve, update, partial_update)',
            'Automaticamente mapea a los URLs usando Routers',
            'Provee mas funcionalidad con menos codigo'
        ]

        return Response({'message': 'Hola', 'a_viewset': a_viewset})
    
    def create(self, request):
        ''' Crear nuevo mensaje de hola mundo '''

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hola {name}'
            return Response({'message': message})
        
        else:
            return Response(serializers.errors, status=status.HTTP_404_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
        ''' Obtiene un objeto y su id'''
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        ''' Actualiza un objeto '''
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        ''' Actualiza parcialmente un objeto '''
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        ''' Actualiza parcialmente un objeto '''
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    ''' Crear y actualizar perfiles '''
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    ''' Crea tokens de autenticacion de usuario '''

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ReadOnlyModelViewSet):
    ''' MAneja el crear leer y actualizar el ProfileFeed '''
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        ''' Configurar el perfil de usuario para el usuario loggeado '''
        serializer.save(user_profile=self.request.user)

