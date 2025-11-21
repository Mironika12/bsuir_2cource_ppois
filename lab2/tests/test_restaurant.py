import pytest

from pizzeria.restaurant.Apron import Apron
from pizzeria.restaurant.CutlerySet import CutlerySet
from pizzeria.restaurant.HighChair import HighChair
from pizzeria.restaurant.MaintenanceRequest import MaintenanceRequest
from pizzeria.restaurant.Menu import Menu
from pizzeria.restaurant.MenuItem import MenuItem
from pizzeria.restaurant.MusicPlaylist import MusicPlaylist
from pizzeria.restaurant.Reservation import Reservation
from pizzeria.restaurant.Table import Table
from pizzeria.restaurant.TableMenuQRCode import TableMenuQRCode
from pizzeria.restaurant.ToySet import ToySet

from exceptions.exceptions import OutOfStockException, InvalidOperationException


def test_apron_initial_state():
    a = Apron("L", "black")
    assert a.is_clean() is True
    assert a.get_info()["assigned_to"] is None


def test_apron_assign_unassign():
    a = Apron("M", "white")
    a.assign_to(10)
    assert a.get_info()["assigned_to"] == 10
    a.unassign()
    assert a.get_info()["assigned_to"] is None


def test_apron_wash():
    a = Apron("S", "red")
    a.mark_dirty()
    assert a.is_clean() is False
    a.wash()
    assert a.is_clean() is True


def test_cutlery_take_and_return():
    c = CutlerySet("SET1", in_stock=2)
    assert c.take_set() is True
    assert c.get_stock() == 1
    c.return_set()
    assert c.get_stock() == 2


def test_cutlery_out_of_stock():
    c = CutlerySet("SET2", in_stock=0)
    with pytest.raises(OutOfStockException):
        c.take_set()


def test_highchair_occupy_and_release():
    h = HighChair("H1")
    h.occupy()
    assert h.get_status() == "occupied"
    h.release()
    assert h.get_status() == "free"


def test_highchair_invalid_occupy():
    h = HighChair("H2")
    h.mark_broken()
    with pytest.raises(InvalidOperationException):
        h.occupy()


def test_maintenance_request_fix():
    m = MaintenanceRequest("Oven", "Broken handle")
    assert m.is_fixed() is False
    msg = m.mark_fixed()
    assert m.is_fixed() is True
    assert "Оборудование 'Oven'" in msg


def test_menu_add_and_find():
    m = Menu([])
    item = MenuItem("Soup", 5.0, "Hot soup")
    m.add_item(item)
    assert m.find_item("Soup") is item


def test_menu_remove():
    item = MenuItem("Tea", 3.0, "Warm tea")
    m = Menu([item])
    assert m.remove_item("Tea") is True
    assert m.find_item("Tea") is None


def test_menuitem_update_price():
    i = MenuItem("Burger", 10.0, "Beef burger")
    i.update_price(12.5)
    assert i.get_price() == 12.5


def test_musicplaylist_add_and_next():
    p = MusicPlaylist("Main", ["A", "B", "C"])
    assert p.get_current() == "A"
    assert p.next_track() == "B"
    assert p.next_track() == "C"
    assert p.next_track() == "A"


def test_musicplaylist_empty():
    p = MusicPlaylist("Empty", [])
    assert p.get_current() is None
    assert p.next_track() is None


def test_reservation_confirm_and_cancel():
    t = Table(1, 4, False)
    r = Reservation(None, t, "18:00")
    assert r.confirm() is True
    assert r.is_confirmed() is True
    assert r.cancel() is True
    assert r.is_confirmed() is False


def test_reservation_confirm_on_reserved_table():
    t = Table(2, 4, True)
    r = Reservation(None, t, "20:00")
    assert r.confirm() is False


def test_table_reserve_free():
    t = Table(5, 2, False)
    assert t.reserve() is True
    assert t.is_reserved() is True
    assert t.free_table() is True
    assert t.is_reserved() is False


def test_qrcode_activation():
    qr = TableMenuQRCode(3, "QRC123")
    assert qr.is_active() is True
    qr.deactivate()
    assert qr.is_active() is False
    qr.activate()
    assert qr.is_active() is True


def test_toyset_checkout_and_return():
    toy = ToySet("T1", "Small toy", in_stock=1)
    assert toy.checkout() is True
    assert toy.get_stock() == 0
    toy.return_toy()
    assert toy.get_stock() == 1


def test_toyset_out_of_stock():
    toy = ToySet("T2", "Doll", in_stock=0)
    with pytest.raises(OutOfStockException):
        toy.checkout()
