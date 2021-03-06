from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from rest_framework.filters import SearchFilter, OrderingFilter

# from store.models import Product
from store.api.serializers import *


@api_view(['GET', ])
def api_detail_user_view(request, username):
    try:
        user = User.objects.get(username=username)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['GET', ])
def api_detail_product_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)


@api_view(['PUT', ])
def api_update_product_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data['success'] = 'Update Successful'
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def api_delete_product_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = product.delete()
        data = {}
        if operation:
            data['success'] = "Successfully Deleted"
        else:
            data['failure'] = 'Failed to Delete'

        return Response(data=data)


@api_view(['POST', ])
def api_create_product_view(request):

    product = Product()

    if request.method == 'POST':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'category', 'slug')


class ApiCategoryListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        return Product.objects.filter(category=self.kwargs['slug'])


class ApiSearchListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'category', 'slug')



######## Hasan's API Views #############
from django.shortcuts import render

# Create your views here.
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import CartUnitSerializer

class CartView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if not bool(request.user.is_anonymous):
            cart_units = request.user.cart_units.all()
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_units = Session.objects.get(session_key=request.session.session_key).cart_units.all()

        return Response(CartUnitSerializer(cart_units.order_by('product__slug'), many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartUnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        product = Product.objects.get(slug=data['slug'])

        cart_unit_data = {
            'product': product,
            'user': None,
            'session': None
        }

        if not bool(request.user.is_anonymous):
            cart_unit_data['user'] = request.user
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_unit_data['session'] = Session.objects.get(session_key=request.session.session_key)

        # # cart_unit = CartUnit.objects.filter(**cart_unit_data).first()
        #
        # if cart_unit is None:
        #     cart_unit = CartUnit(**cart_unit_data)
        #
        # cart_unit.quantity = data['quantity']
        # cart_unit.save()

        return Response(status=status.HTTP_201_CREATED)


class CartUnitView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, slug=None):
        if not bool(request.user.is_anonymous):
            cart_units = request.user.cart_units.all()
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_units = Session.objects.get(session_key=request.session.session_key).cart_units.all()

        cart_unit = cart_units.filter(product__slug=slug).first()

        if cart_unit is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_unit.delete()

        return Response(status=status.HTTP_200_OK)


from rest_framework.permissions import AllowAny, IsAuthenticated




class OrderView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user

        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        queryset = Order.objects.filter(user=user)
        serializer = OrderListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        if not bool(request.user.is_anonymous):
            cart_units = request.user.cart_units.all()
            data['user'] = request.user

            # DeliveryInfoService.delete_by_user(request.user)
            # DeliveryInfo.objects.create(**data)
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_units = Session.objects.get(session_key=request.session.session_key).cart_units.all()
            data['user'] = None

        if cart_units.count() == 0:
            raise serializers.ValidationError('Cart is empty, nothing to order')

        order = Order.objects.create(**data)

        for cart_unit in cart_units:
            if cart_unit.unit.num_in_stock < cart_unit.quantity:
                raise serializers.ValidationError(
                    'Not enough units in stock: {}'.format(cart_unit.unit.sku)
                )

        for cart_unit in cart_units:
            unit = cart_unit.unit

            # OrderUnit.objects.create(
            #     order=order,
            #     quantity=cart_unit.quantity,
            #     unit=unit,
            #     unit_price=unit.price
            # )

            unit.num_in_stock -= cart_unit.quantity
            unit.save()

            # Clear cart
            cart_unit.delete()

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        user = request.user
        order = Order.objects.get(pk=pk)

        if user.id != order.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import ProductListSerializer, RatingSerializer, ReviewSerializer


# from rest_framework.decorators import action
# from rest_framework import permissions
from rest_framework import viewsets


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class RatingViewSet(viewsets.ModelViewSet):
    # queryset = Ratings.objects.all()
    serializer_class = RatingSerializer





class ProductSetPagination(PageNumberPagination):
    page_size = 32

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'page': self.page.number,
                'has_prev': self.page.has_previous(),
                'has_next': self.page.has_next(),
            },
            'data': data
        })


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        q = self.request.query_params.get('q', None)
        tags = self.request.query_params.get('tags')
        in_stock = self.request.query_params.get('in_stock', None)

        if q is not None:
            queryset = queryset.filter(title__icontains=q)

        if tags:
            tags = tags.split(',')

            for tag in tags:
                queryset = queryset.filter(tag_set__name__iexact=tag).distinct()

        if in_stock == '1':
            queryset = queryset.filter(unit__num_in_stock__gt=0).distinct()

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer