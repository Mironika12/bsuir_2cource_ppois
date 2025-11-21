import pytest

# Imports from your project
from pizzeria.core.Customer import Customer
from pizzeria.core.Address import Address
from pizzeria.core.Employee import Employee
from pizzeria.restaurant.MenuItem import MenuItem

from pizzeria.customer.Cart import Cart
from pizzeria.customer.Feedback import Feedback
from pizzeria.customer.Notification import Notification
from pizzeria.customer.Review import Review
from pizzeria.customer.ReviewManager import ReviewManager


# ======================================================
#                  TEST Cart
# ======================================================

def make_customer():
    return Customer("Alice", "123", "mail@mail.com", Address("Street", "City", "000"))


def make_menu_item():
    return MenuItem("Pizza", 10.0, "Tasty pizza")


def test_cart_add_and_get_items():
    customer = make_customer()
    cart = Cart(customer, [])

    item = make_menu_item()
    cart.add_item(item)

    assert len(cart.get_items()) == 1
    assert cart.get_items()[0] is item


def test_cart_clear():
    customer = make_customer()
    cart = Cart(customer, [make_menu_item(), make_menu_item()])

    cart.clear_cart()
    assert len(cart.get_items()) == 0


def test_cart_customer_returned():
    customer = make_customer()
    cart = Cart(customer, [])
    assert cart.get_customer() is customer


# ======================================================
#                  TEST Feedback
# ======================================================

def test_feedback_getters():
    fb = Feedback("Very tasty!", "food")
    assert fb.get_text() == "Very tasty!"
    assert fb.get_category() == "food"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("I love this!", "positive"),
        ("The food was awful", "negative"),
        ("Just okay", "neutral"),
    ]
)
def test_feedback_sentiment(text, expected):
    fb = Feedback(text, "general")
    assert fb.analyze_sentiment() == expected


# ======================================================
#                  TEST Notification
# ======================================================

def test_notification_send_to_customer():
    customer = make_customer()
    notif = Notification("Your order is ready", customer)

    assert notif.is_sent() is False
    assert notif.send() is True
    assert notif.is_sent() is True

    # повторная отправка — не отправляется
    assert notif.send() is False


def test_notification_send_to_employee():
    emp = Employee(1, "Bob", "111", "chef", 1000)
    notif = Notification("Start shift", emp)

    assert notif.send() is True
    assert notif.get_recipient() is emp


# ======================================================
#                  TEST Review
# ======================================================

def test_review_getters():
    customer = make_customer()
    r = Review(customer, 5, "Excellent!")

    assert r.get_customer() is customer
    assert r.get_rating() == 5
    assert r.get_comment() == "Excellent!"


def test_review_edit_comment():
    customer = make_customer()
    r = Review(customer, 4, "Good")

    r.edit_comment("Updated comment")
    assert r.get_comment() == "Updated comment"

    # пустая строка не должна менять комментарий
    r.edit_comment("   ")
    assert r.get_comment() == "Updated comment"


# ======================================================
#                  TEST ReviewManager
# ======================================================

def test_review_manager_add_and_average():
    rm = ReviewManager([])

    c = make_customer()
    r1 = Review(c, 5, "Great")
    r2 = Review(c, 3, "Okay")

    rm.add_review(r1)
    rm.add_review(r2)

    assert len(rm.reviews) == 2
    assert rm.get_average_rating() == 4.0


def test_review_manager_empty_average():
    rm = ReviewManager([])
    assert rm.get_average_rating() == 0.0
