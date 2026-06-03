import logging

import pandas as pd
from django.contrib.auth.models import User

from restaurant.models import Booking, Category, MenuItem, Order, OrderItem


def run():

    # set up logging
    lgr = logging.getLogger()
    lgr.setLevel(logging.INFO)

    logging.info("Loading Categories ...")
    # read csv file and iterate through the data and create model instances
    menu_item_fpath = "restaurant/static/data/categories.csv"
    menu_item_data = pd.read_csv(menu_item_fpath, encoding="utf-8")
    for index, row in menu_item_data.iterrows():
        # create the instance
        category = Category.objects.get_or_create(title=row["title"])

    logging.info("Loading Menu Items ...")
    # read csv file and iterate through the data and create model instances
    menu_item_fpath = "restaurant/static/data/menu_items.csv"
    menu_item_data = pd.read_csv(menu_item_fpath, encoding="utf-8")
    for index, row in menu_item_data.iterrows():
        # create the instance
        menuitem = MenuItem.objects.get_or_create(
            name=row["name"],
            price=float(row["price"]),
            quantity=int(row["quantity"]),
            ingredients=row["ingredients"],
            description=row["description"],
            featured=row["featured"],
            category_id=Category.objects.get(pk=row["category_id"]),
            created_date_time=row["created_date_time"],
            reference=row["reference"],
        )

    logging.info("Loading Bookings ...")
    # read csv file and iterate through the data and create model instances
    booking_fpath = "restaurant/static/data/bookings.csv"
    booking_data = pd.read_csv(booking_fpath, encoding="utf-8")
    for index, row in booking_data.iterrows():
        # create the instance
        booking = Booking.objects.get_or_create(
            full_name=row["full_name"],
            mobile_number=row["mobile_number"],
            guest_number=int(row["guest_number"]),
            date_time=row["date_time"],
            comment=row["comment"],
        )

    logging.info("Loading Users ...")
    # read csv file and iterate through the data and create model instances
    users_fpath = "restaurant/static/data/users.csv"
    users_data = pd.read_csv(users_fpath, encoding="utf-8")
    for index, row in users_data.iterrows():
        if row["is_super_user"] and (
            not User.objects.filter(username=row["username"]).exists()
        ):
            # create the instance
            user = User.objects.create_superuser(
                username=row["username"],
                password=row["password"],
                email=row["email"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                is_staff=row["is_staff_user"],
            )
        if not row["is_super_user"]:
            # create the instance
            user = User.objects.get_or_create(
                username=row["username"],
                password=row["password"],
                email=row["email"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                is_staff=row["is_staff_user"],
            )

    logging.info("Loading Orders ...")
    # read csv file and iterate through the data and create model instances
    order_fpath = "restaurant/static/data/orders.csv"
    order_data = pd.read_csv(order_fpath, encoding="utf-8")
    for index, row in order_data.iterrows():
        # create the instance
        order = Order.objects.get_or_create(
            customer_username=User.objects.get(username=row["customer_username"]),
            delivery_username=User.objects.get(username=row["delivery_username"]),
            status=row["status"],
            total=float(row["total"]),
            date_time=row["date_time"],
        )

    logging.info("Loading OrderItems ...")
    # read csv file and iterate through the data and create model instances
    order_items_fpath = "restaurant/static/data/orderitems.csv"
    order_items_data = pd.read_csv(order_items_fpath, encoding="utf-8")
    for index, row in order_items_data.iterrows():
        # create the instance
        order = OrderItem.objects.get_or_create(
            order_id=Order.objects.get(pk=row["order_id"]),
            menuitem_id=MenuItem.objects.get(pk=row["menuitem_id"]),
            quantity=int(row["quantity"]),
            price=float(row["price"]),
        )
