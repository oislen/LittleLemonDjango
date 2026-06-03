from random import randint

from restaurant.models import Booking, Category, MenuItem

BOOKINGS = {
    1: {
        "full_name": "Adam Byrne",
        "mobile_number": "1234567",
        "guest_number": randint(1, 11),
        "date_time": "2023-03-04 09:00:00",
        "comment": "Wedding",
    },
    2: {
        "full_name": "Jake Nelson",
        "mobile_number": "2345678",
        "guest_number": randint(1, 11),
        "date_time": "2024-01-10 12:00:00",
        "comment": "Funeral",
    },
    3: {
        "full_name": "Sinead Bughes",
        "mobile_number": "3456789",
        "guest_number": randint(1, 11),
        "date_time": "2025-12-20 14:00:00",
        "comment": "Christening",
    },
}

MENU_ITEMS = {
    1: {
        "name": "Apple Pie",
        "price": 13.78,
        "quantity": randint(0, 11),
        "description": "Baked apple pie with cream",
        "category": "Dessert",
        "created_date_time": "2023-03-04 09:00:00",
        "reference": "APLPIE20230304",
    },
    2: {
        "name": "Vanilla Latte",
        "price": 3.99,
        "quantity": randint(0, 11),
        "description": "Barista latte with vanilla essence",
        "category": "Drinks",
        "created_date_time": "2023-03-04 12:00:00",
        "reference": "VANLTE20230304",
    },
    3: {
        "name": "Ice-cream",
        "price": 5.00,
        "quantity": randint(0, 11),
        "description": "Chocolate, strawberry ot vanilla",
        "category": "Dessert",
        "created_date_time": "2023-03-04 14:00:00",
        "reference": "ICECRM20230304",
    },
}


class BookingMixin:
    bookings = BOOKINGS

    def create_bookings(self):
        for idx in self.bookings.keys():
            booking = Booking.objects.create(
                full_name=self.bookings[idx]["full_name"],
                mobile_number=self.bookings[idx]["mobile_number"],
                guest_number=self.bookings[idx]["guest_number"],
                date_time=self.bookings[idx]["date_time"],
                comment=self.bookings[idx].get("comment", None),
            )
            booking.save()


class SingleBookingMixin:
    booking = BOOKINGS.get(1)

    def create_booking(self):
        booking = Booking.objects.create(
            full_name=self.booking.get("full_name"),
            mobile_number=self.booking.get("mobile_number"),
            guest_number=self.booking.get("guest_number"),
            date_time=self.booking.get("date_time"),
            comment=self.booking.get("comment", None),
        )
        booking.save()
        self.booking = booking


class MenuItemMixin:
    items = MENU_ITEMS

    def create_menu_items(self):
        for idx in self.items.keys():
            # create category
            category = Category.objects.create(title=self.items[idx].get("category"))
            # create menu item
            item = MenuItem.objects.create(
                name=self.items[idx]["name"],
                price=self.items[idx]["price"],
                quantity=self.items[idx].get("quantity", None),
                description=self.items[idx].get("description", None),
                featured=self.items[idx].get("featured", False),
                category_id=category,
                created_date_time=self.items[idx].get("created_date_time", None),
                reference=self.items[idx].get("reference", None),
            )
            item.save()


class SingleMenuItemMixin:
    item = MENU_ITEMS.get(1)

    def create_menu_item(self):
        # create category
        category = Category.objects.create(title=self.item.get("category"))
        # create menu item
        item = MenuItem.objects.create(
            name=self.item["name"],
            price=self.item["price"],
            description=self.item.get("description", None),
            quantity=self.item.get("quantity", None),
            featured=self.item.get("featured", False),
            category_id=category,
            created_date_time=self.item.get("created_date_time", None),
            reference=self.item.get("reference", None),
        )
        item.save()
        self.menu_item = item
