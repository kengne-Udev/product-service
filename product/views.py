from rest_framework import generics, status
from product.utils import validate_jwt
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductListCreateAPIView(APIView):
    
    def get(self, request):
        authorization = request.headers.copy()["Authorization"]
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            payload = validate_jwt(token)
            if payload:
                products = Product.objects.all()
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    

    def post(self, request):
        return Response({'success': 'ok'})


class ProductDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
