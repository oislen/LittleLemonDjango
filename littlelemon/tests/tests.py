import json
from decimal import Decimal

from api.permissions import IsDeliveryCrew, IsManager
from api.serializers import (
    BookingSerializer,
    CartSerializer,
    CategorySerializer,
    MenuItemSerializer,
    OrderSerializer,
)
from django.contrib.auth.models import Group, User
from django.test import RequestFactory, TestCase
from restaurant.models import Booking, Category, MenuItem, Order

from tests.mixins import (
    BookingMixin,
    CategoryMixin,
    MenuItemMixin,
    OrderMixin,
    SingleBookingMixin,
    SingleCategoryMixin,
    SingleMenuItemMixin,
    SingleOrderMixin,
)


class SetUpMixin:
    def setUp(self):
        username = "test@email.com"
        password = "testpasswd"
        # create test user
        self.user = User.objects.create_user(username=username, password=password)
        # log in to django client as test user
        self.login = self.client.login(username=username, password=password)


class BookingViewTest(SetUpMixin, BookingMixin, TestCase):
    def setUp(self):
        self.create_bookings()
        return super().setUp()

    def test_list(self):
        response = self.client.get("/api/bookings/")
        serializer = BookingSerializer(Booking.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        data = {
            "full_name": "jack doe",
            "mobile_number": "1234567",
            "guest_number": 4,
            "date_time": "2023-03-04 09:00:00",
            "comment": "18th Birthday",
        }
        response = self.client.post("/api/bookings/", data=data)
        serializer = BookingSerializer(Booking.objects.get(full_name="jack doe"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)


class SingleBookingViewTest(SetUpMixin, SingleBookingMixin, TestCase):
    def setUp(self):
        self.create_booking()
        return super().setUp()

    def test_retrieve(self):
        response = self.client.get(f"/api/bookings/{self.booking.pk}/")
        serializer = BookingSerializer(Booking.objects.get(pk=self.booking.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update(self):
        data = json.dumps({"guest_number": 6, "date_time": "2023-03-06 10:00"})
        response = self.client.patch(
            f"/api/bookings/{self.booking.pk}/",
            data=data,
            content_type="application/json",
        )
        serializer = BookingSerializer(Booking.objects.get(pk=self.booking.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update(self):
        data = json.dumps(
            {
                "full_name": "will gleeson",
                "mobile_number": "2345678",
                "guest_number": 6,
                "date_time": "2023-03-06 18:00:00",
            }
        )
        response = self.client.put(
            f"/api/bookings/{self.booking.pk}/",
            data=data,
            content_type="application/json",
        )
        serializer = BookingSerializer(Booking.objects.get(pk=self.booking.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(f"/api/bookings/{self.booking.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        self.assertEqual(Booking.objects.filter(pk=self.booking.pk).exists(), False)


class MenuItemViewTest(SetUpMixin, MenuItemMixin, TestCase):
    def setUp(self):
        self.create_menu_items()
        super().setUp()

    def test_list(self):
        response = self.client.get("/api/menu-items/")
        serializer = MenuItemSerializer(MenuItem.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        data = {
            "name": "Ice Latte",
            "price": 2.99,
            "quantity": 5,
            "description": "Finely grounded and on ice.",
            "featured": False,
            "category_id": 1,
            "created_date_time": "2024-12-07",
            "reference": "ICELTE20241207",
        }
        response = self.client.post(
            "/api/menu-items/", data=data, content_type="application/json"
        )
        serializer = MenuItemSerializer(MenuItem.objects.get(name="Ice Latte"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)


class SingleMenuItemViewTest(SetUpMixin, SingleMenuItemMixin, TestCase):
    def setUp(self):
        self.create_menu_item()
        return super().setUp()

    def test_retrieve(self):
        response = self.client.get(f"/api/menu-items/{self.menu_item.pk}/")
        serializer = MenuItemSerializer(MenuItem.objects.get(pk=self.menu_item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update(self):
        data = json.dumps({"price": 3.99, "quantity": 3})
        response = self.client.patch(
            f"/api/menu-items/{self.menu_item.pk}/",
            data=data,
            content_type="application/json",
        )
        serializer = MenuItemSerializer(MenuItem.objects.get(pk=self.menu_item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update(self):
        data = json.dumps(
            {
                "name": "Apple Juice",
                "price": 3.85,
                "quantity": 7,
                "description": "Freshly squeezed",
                "category_id": 1,
                "created_date_time": "2024-12-07 10:00:00",
                "reference": "APLJCE20241207",
            }
        )
        response = self.client.put(
            f"/api/menu-items/{self.menu_item.pk}/",
            data=data,
            content_type="application/json",
        )
        serializer = MenuItemSerializer(MenuItem.objects.get(pk=self.menu_item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(f"/api/menu-items/{self.menu_item.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        self.assertEqual(MenuItem.objects.filter(pk=self.menu_item.pk).exists(), False)


# ---------------------------------------------------------------------------
# Category API
# ---------------------------------------------------------------------------
class CategoryViewTest(SetUpMixin, CategoryMixin, TestCase):
    def setUp(self):
        self.create_categories()
        return super().setUp()

    def test_list(self):
        response = self.client.get("/api/categories/")
        serializer = CategorySerializer(Category.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        data = {"title": "Specials"}
        response = self.client.post("/api/categories/", data=data)
        serializer = CategorySerializer(Category.objects.get(title="Specials"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)


class SingleCategoryViewTest(SetUpMixin, SingleCategoryMixin, TestCase):
    def setUp(self):
        self.create_category()
        return super().setUp()

    def test_retrieve(self):
        response = self.client.get(f"/api/categories/{self.category.pk}/")
        serializer = CategorySerializer(Category.objects.get(pk=self.category.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update(self):
        data = json.dumps({"title": "Renamed"})
        response = self.client.put(
            f"/api/categories/{self.category.pk}/",
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.title, "Renamed")

    def test_delete(self):
        response = self.client.delete(f"/api/categories/{self.category.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.filter(pk=self.category.pk).exists(), False)


# ---------------------------------------------------------------------------
# Order API
# ---------------------------------------------------------------------------
class OrderViewTest(SetUpMixin, OrderMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.create_orders()

    def test_list(self):
        response = self.client.get("/api/orders/")
        serializer = OrderSerializer(Order.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        data = {
            "customer_username": self.user.pk,
            "total": "30.00",
            "date_time": "2026-02-01 18:00:00",
        }
        response = self.client.post(
            "/api/orders/", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        # status defaults to "pending" and the order is owned by the test user
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(response.data["customer_username"], self.user.pk)


class SingleOrderViewTest(SetUpMixin, SingleOrderMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.create_order()

    def test_retrieve(self):
        response = self.client.get(f"/api/orders/{self.order.pk}/")
        serializer = OrderSerializer(Order.objects.get(pk=self.order.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update_status(self):
        data = json.dumps({"status": "delivered"})
        response = self.client.patch(
            f"/api/orders/{self.order.pk}/",
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "delivered")

    def test_delete(self):
        response = self.client.delete(f"/api/orders/{self.order.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Order.objects.filter(pk=self.order.pk).exists(), False)


# ---------------------------------------------------------------------------
# Negative / edge cases on the existing API endpoints
# ---------------------------------------------------------------------------
class ApiEdgeCaseTest(SetUpMixin, SingleBookingMixin, TestCase):
    def setUp(self):
        self.create_booking()
        return super().setUp()

    def test_retrieve_missing_booking_returns_404(self):
        response = self.client.get("/api/bookings/999999/")
        self.assertEqual(response.status_code, 404)

    def test_create_booking_missing_required_field_returns_400(self):
        # guest_number, date_time and mobile_number are required
        data = {"full_name": "No Details"}
        response = self.client.post("/api/bookings/", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Booking.objects.filter(full_name="No Details").exists())

    def test_delete_missing_booking_returns_404(self):
        response = self.client.delete("/api/bookings/999999/")
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class ModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(title="Sides")
        self.assertEqual(category.title, "Sides")
        self.assertIsNotNone(category.pk)

    def test_menu_item_defaults(self):
        category = Category.objects.create(title="Sides")
        item = MenuItem.objects.create(
            reference="GRKSAL20260101",
            name="Greek Salad",
            category_id=category,
            created_date_time="2026-01-01 10:00:00",
        )
        # optional fields default to None and featured defaults to False
        self.assertIsNone(item.description)
        self.assertIsNone(item.price)
        self.assertIsNone(item.quantity)
        self.assertFalse(item.featured)

    def test_booking_comment_optional(self):
        booking = Booking.objects.create(
            full_name="Jane Doe",
            mobile_number="1234567",
            guest_number=2,
            date_time="2026-01-01 10:00:00",
        )
        self.assertIsNone(booking.comment)

    def test_order_status_default(self):
        user = User.objects.create_user(username="cust@email.com", password="pw")
        order = Order.objects.create(
            customer_username=user,
            total="12.00",
            date_time="2026-01-01 10:00:00",
        )
        self.assertEqual(order.status, "pending")
        self.assertIsNone(order.delivery_username)


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------
class CartSerializerTest(TestCase):
    def test_validate_computes_price(self):
        """CartSerializer.validate derives price from quantity * unit_price."""
        attrs = {"quantity": 3, "unit_price": Decimal("2.50")}
        result = CartSerializer().validate(attrs)
        self.assertEqual(result["price"], Decimal("7.50"))


# ---------------------------------------------------------------------------
# Custom permission classes
# ---------------------------------------------------------------------------
class PermissionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="member@email.com", password="pw"
        )

    def _request_for(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_is_manager_grants_group_member(self):
        self.user.groups.add(Group.objects.create(name="Manager"))
        self.assertTrue(IsManager().has_permission(self._request_for(self.user), None))

    def test_is_manager_denies_non_member(self):
        self.assertFalse(
            IsManager().has_permission(self._request_for(self.user), None)
        )

    def test_is_delivery_crew_grants_group_member(self):
        self.user.groups.add(Group.objects.create(name="Delivery Crew"))
        self.assertTrue(
            IsDeliveryCrew().has_permission(self._request_for(self.user), None)
        )

    def test_is_delivery_crew_denies_non_member(self):
        self.assertFalse(
            IsDeliveryCrew().has_permission(self._request_for(self.user), None)
        )


# ---------------------------------------------------------------------------
# Custom API views
# ---------------------------------------------------------------------------
class AssignManagerViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin@email.com", password="pw", email="admin@email.com"
        )
        self.client.login(username="admin@email.com", password="pw")
        self.target = User.objects.create_user(
            username="target@email.com", password="pw"
        )

    def test_admin_can_assign_user_to_manager_group(self):
        response = self.client.post(
            "/api/assign-manager/", data={"user_id": self.target.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.target.groups.filter(name="Manager").exists())

    def test_non_admin_is_forbidden(self):
        self.client.logout()
        self.client.login(username="target@email.com", password="pw")
        response = self.client.post(
            "/api/assign-manager/", data={"user_id": self.admin.pk}
        )
        self.assertIn(response.status_code, (401, 403))


# ---------------------------------------------------------------------------
# Restaurant server-rendered views
# ---------------------------------------------------------------------------
class RestaurantViewTest(TestCase):
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_about(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

    def test_book_get_renders_form(self):
        response = self.client.get("/book/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book.html")
        self.assertIn("form", response.context)

    def test_book_post_creates_booking(self):
        data = {
            "full_name": "Web Booker",
            "mobile_number": "1234567",
            "guest_number": 3,
            "date_time": "2026-03-04 09:00:00",
        }
        response = self.client.post("/book/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Booking.objects.filter(full_name="Web Booker").exists())

    def test_menu_lists_only_featured_items(self):
        category = Category.objects.create(title="Main")
        featured = MenuItem.objects.create(
            reference="FEAT20260101",
            name="Featured Dish",
            category_id=category,
            created_date_time="2026-01-01 10:00:00",
            featured=True,
        )
        MenuItem.objects.create(
            reference="HID20260101",
            name="Hidden Dish",
            category_id=category,
            created_date_time="2026-01-01 10:00:00",
            featured=False,
        )
        response = self.client.get("/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu.html")
        menu = list(response.context["menu"])
        self.assertIn(featured, menu)
        self.assertEqual(len(menu), 1)

    def test_display_menu_item_with_existing_image(self):
        # "Bruschetta" has a matching image under static/img/menu_items
        category = Category.objects.create(title="Main")
        item = MenuItem.objects.create(
            reference="BRU20260101",
            name="Bruschetta",
            category_id=category,
            created_date_time="2026-01-01 10:00:00",
        )
        response = self.client.get(f"/menu_item/{item.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu_item.html")
        self.assertEqual(response.context["menu_item"], item)

    def test_display_menu_item_without_image_falls_back(self):
        # A name with no matching image leaves the default (empty) menu_item
        category = Category.objects.create(title="Main")
        item = MenuItem.objects.create(
            reference="NOIMG20260101",
            name="No Image Dish",
            category_id=category,
            created_date_time="2026-01-01 10:00:00",
        )
        response = self.client.get(f"/menu_item/{item.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["menu_item"], "")


# ---------------------------------------------------------------------------
# Delivery-crew order workflow (custom APIViews)
# ---------------------------------------------------------------------------
class DeliveryCrewOrderViewTest(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer@email.com", password="pw"
        )
        self.crew = User.objects.create_user(username="crew@email.com", password="pw")
        self.crew.groups.add(Group.objects.create(name="Delivery Crew"))
        self.other_crew = User.objects.create_user(
            username="other@email.com", password="pw"
        )

        # pending order assigned to our crew member
        self.pending_order = Order.objects.create(
            customer_username=self.customer,
            delivery_username=self.crew,
            status="pending",
            total="10.00",
            date_time="2026-01-01 12:00:00",
        )
        # already-delivered order assigned to our crew member
        self.delivered_order = Order.objects.create(
            customer_username=self.customer,
            delivery_username=self.crew,
            status="delivered",
            total="20.00",
            date_time="2026-01-01 12:00:00",
        )
        # pending order assigned to someone else
        self.other_order = Order.objects.create(
            customer_username=self.customer,
            delivery_username=self.other_crew,
            status="pending",
            total="30.00",
            date_time="2026-01-01 12:00:00",
        )

    def test_get_returns_only_own_pending_orders(self):
        self.client.login(username="crew@email.com", password="pw")
        response = self.client.get("/api/delivery-orders/")
        self.assertEqual(response.status_code, 200)
        returned_ids = [order["order_id"] for order in response.data]
        self.assertEqual(returned_ids, [self.pending_order.pk])

    def test_get_forbidden_for_non_delivery_crew(self):
        self.client.login(username="customer@email.com", password="pw")
        response = self.client.get("/api/delivery-orders/")
        self.assertEqual(response.status_code, 403)

    def test_patch_marks_own_order_delivered(self):
        self.client.login(username="crew@email.com", password="pw")
        response = self.client.patch(
            f"/api/delivery-orders/{self.pending_order.pk}/"
        )
        self.assertEqual(response.status_code, 200)
        self.pending_order.refresh_from_db()
        self.assertEqual(self.pending_order.status, "delivered")

    def test_patch_order_assigned_to_other_returns_404(self):
        self.client.login(username="crew@email.com", password="pw")
        response = self.client.patch(
            f"/api/delivery-orders/{self.other_order.pk}/"
        )
        self.assertEqual(response.status_code, 404)
        self.other_order.refresh_from_db()
        self.assertEqual(self.other_order.status, "pending")


class AssignToDeliveryCrewTest(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer@email.com", password="pw"
        )
        self.crew = User.objects.create_user(username="crew@email.com", password="pw")
        self.manager = User.objects.create_user(
            username="manager@email.com", password="pw"
        )
        self.manager.groups.add(Group.objects.create(name="Manager"))
        self.order = Order.objects.create(
            customer_username=self.customer,
            total="15.00",
            date_time="2026-01-01 12:00:00",
        )

    def test_manager_assigns_delivery_crew(self):
        self.client.login(username="manager@email.com", password="pw")
        response = self.client.post(
            "/api/assign-delivery-crew/",
            data={"user_id": self.crew.pk, "order_id": self.order.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.delivery_username, self.crew)

    def test_non_manager_is_forbidden(self):
        self.client.login(username="customer@email.com", password="pw")
        response = self.client.post(
            "/api/assign-delivery-crew/",
            data={"user_id": self.crew.pk, "order_id": self.order.pk},
        )
        self.assertEqual(response.status_code, 403)
        self.order.refresh_from_db()
        self.assertIsNone(self.order.delivery_username)
