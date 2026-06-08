from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AssignToDeliveryCrew,
    AssignUserToManagerGroup,
    BookingViewSet,
    CategoryViewSet,
    CustomerOrderViewSet,
    DeliveryCrewOrderView,
    MenuItemViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("menu-items", MenuItemViewSet, basename="menu-items")
router.register("orders", CustomerOrderViewSet, basename="orders")
router.register("bookings", BookingViewSet, basename="bookings")
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("assign-manager/", AssignUserToManagerGroup.as_view(), name="assign-manager"),
    path(
        "assign-delivery-crew/",
        AssignToDeliveryCrew.as_view(),
        name="assign-delivery-crew",
    ),
    path("delivery-orders/", DeliveryCrewOrderView.as_view(), name="delivery-orders"),
    path(
        "delivery-orders/<int:order_id>/",
        DeliveryCrewOrderView.as_view(),
        name="delivery-order-detail",
    ),
]
