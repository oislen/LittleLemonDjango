from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from restaurant.models import Booking, Category, MenuItem, Order

from .serializers import (
    BookingSerializer,
    CategorySerializer,
    MenuItemSerializer,
    OrderSerializer,
    UserSerializer,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerOrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class DeliveryCrewOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.groups.filter(name="Delivery Crew").exists():
            orders = Order.objects.filter(delivery_crew=request.user, status=False)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        return Response({"error": "Unauthorized"}, status=403)

    def patch(self, request, order_id):
        order = Order.objects.get(id=order_id, delivery_crew=request.user)
        order.status = True
        order.save()
        return Response({"message": "Order marked as delivered"})


class AssignUserToManagerGroup(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        manager_group.user_set.add(user)
        return Response({"message": "User assigned to Manager group"})


class AssignToDeliveryCrew(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.groups.filter(name="Manager").exists():
            user_id = request.data.get("user_id")
            order_id = request.data.get("order_id")
            user = User.objects.get(id=user_id)
            order = Order.objects.get(id=order_id)
            order.delivery_crew = user
            order.save()
            return Response({"message": "Order assigned to delivery crew"})
        return Response({"error": "Unauthorized"}, status=403)
