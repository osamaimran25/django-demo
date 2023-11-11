from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Q

from .models import Product
from .serializer import ProductSerializer

class ProductAPIView(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        try:
            search_query = request.query_params.get('search', '')
            sort_by = request.query_params.get('sort_by', '')
            sort_order = request.query_params.get('sort_order', 'asc')  # Default to ascending order

            if search_query:
                products = Product.objects.filter(
                    Q(name__icontains=search_query) | Q(description__icontains=search_query)
                )

                if sort_by in ['id', 'name', 'description', 'stock', 'price']:
                    if sort_order == 'desc':
                        sort_by = f'-{sort_by}'  
                    products = products.order_by(sort_by)
                else:
                    products = products.order_by('id')

                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
            else:
                return Response("Please provide a search query parameter.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"An error occurred during the search: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    @action(detail=False, methods=['get'])
    def selected_product(self, request):
        try:
            ids = request.query_params.get('ids', "")
            if not ids:
                return Response("Please provide a list of product IDs.", status=status.HTTP_400_BAD_REQUEST)
            ids =  [int(num) for num in ids.split(',')]           
            search_query = request.query_params.get('search', '')
            products = Product.objects.filter(id__in=ids)
            # if search_query:
            #     products = products.filter(
            #         Q(name__icontains=search_query) | Q(description__icontains=search_query)
            #     )
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(f"An error occurred while fetching selected products: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)