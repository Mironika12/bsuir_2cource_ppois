# README: Система Управления Пиццерией (Pizza Management System)

- Классы: 50
- Поля: 130
- Уникальные поведения: 179
- Ассоциации: 35
- Исключения: 23

## Исключения (23)
Все исключения находятся в модуле `exceptions.py`:

- PizzaException (базовое исключение)
- IngredientException
- InvalidIngredientException
- OutOfStockException
- IngredientNotFoundException
- OrderException
- OrderNotFoundException
- OrderNotReadyException
- PaymentException
- PaymentFailedException
- SupplierException
- SupplierProductException
- NegativeAmountException
- MenuException
- MenuItemNotFoundException
- InvalidCouponException
- EmployeeException
- EmployeeNotFoundException
- SelfActionException
- UnauthorizedAccessException
- KitchenOverloadException
- ValidationException
- NegativeHoursException
- InvalidOperationException

## Классы
Формат: Класс Поля Методы → Ассоциации (классы как поля/параметры)

### Бизнес-логика (Business)
Coupon 3 5
- Поля: _code, _discount_percent, _active
- Методы: get_code, get_discount_percent, is_active, validate, deactivate

DailySalesReport 0 1 → Report
- Методы: summarize_sales

DiscountPolicy 2 1
- Поля: threshold, discount
- Методы: apply

InventoryReport 0 1 → Report
- Методы: summarize_stock

LoyaltyCard 4 9 → Customer
- Поля: _owner, _points, _tier, _history
- Методы: _calculate_tier, _update_tier, add_points, redeem_points, get_owner, get_points, get_tier, get_history, get_summary

Promotion 3 5
- Поля: _name, _description, _active
- Методы: get_name, get_description, is_active, activate, deactivate

Report 2 3
- Поля: _title, _data
- Методы: get_title, get_data, generate_pdf

Statistic 2 3
- Поля: _name, _value
- Методы: get_name, get_value, update_value

### Основные классы (Core)
Address 3 4
- Поля: _street, _city, _zip_code
- Методы: format_address, get_street, get_city, get_zip_code

Chef 0 2 → Pizza, Ingredient
- Методы: prepare_pizza, check_ingredients

Cleaner 2 4
- Поля: _assigned_zones, _completed_tasks
- Методы: assign_zone, get_assigned_zones, complete_cleaning, get_completed_tasks

Courier 2 3
- Поля: _vehicle_type, _deliveries_completed
- Методы: complete_delivery, get_vehicle_type, get_deliveries_completed

Customer 4 4 → Address
- Поля: _name, _phone, _email, _address
- Методы: get_name, get_phone, get_email, get_address

Delivery 6 8 → Order, Courier, Address
- Поля: _delivery_id, _order, _courier, _address, _status, _estimated_time
- Методы: calculate_estimated_time, update_status, get_delivery_id, get_order, get_courier, get_address, get_status, get_estimated_time

Employee 6 8
- Поля: _employee_id, _name, _phone, _role, _salary, _work_hours
- Методы: add_work_hours, calculate_monthly_payment, get_employee_id, get_name, get_role, get_phone, get_salary, get_work_hours

Ingredient 4 6
- Поля: _name, _quantity, _unit, _cost
- Методы: decrease_stock, restock, get_name, get_quantity, get_unit, get_cost

InStoreOrder 1 1 → Table
- Поля: _table
- Методы: assign_table

Inventory 1 3 → Ingredient
- Поля: items
- Методы: add_item, remove_item, check_stock

Manager 0 2 → Coupon, Employee
- Методы: approve_discount, fire_employee

OnlineOrder 1 2 → Address
- Поля: _address
- Методы: request_delivery, track_order

Order 5 8 → Customer, Pizza
- Поля: _order_id, _customer, _pizzas, _status, _total_price
- Методы: calculate_total, update_status, apply_discount, get_order_id, get_customer, get_pizzas, get_status, get_total_price

OrderQueue 1 2 → Order
- Поля: queue
- Методы: enqueue, dequeue

Oven 4 3
- Поля: _oven_id, _capacity, _loaded, _running_tasks
- Методы: load_pizza, unload_ready, get_status

Payment 5 7
- Поля: _payment_id, _amount, _method, _status, _transaction_code
- Методы: process, refund, get_payment_id, get_amount, get_method, get_status, get_transaction_code

Pizza 5 8 → Ingredient
- Поля: _name, _size, _crust, _price, _ingredients
- Методы: calculate_calories, add_ingredient, remove_ingredient, get_name, get_size, get_crust, get_price, get_ingredients

PizzaBox 4 5
- Поля: _size, _material, _printed_label, _sealed
- Методы: seal, unseal, is_sealed, set_label, get_info

Waiter 0 2 → Customer, Order
- Методы: take_order, serve_order

### Клиентская часть (Customer)
Cart 2 4 → Customer, MenuItem
- Поля: _customer, _items
- Методы: get_customer, get_items, add_item, clear_cart

Feedback 2 3
- Поля: _text, _category
- Методы: get_text, get_category, analyze_sentiment

Notification 3 4 → Customer, Employee
- Поля: _message, _recipient, _sent
- Методы: get_message, get_recipient, is_sent, send

Review 3 4 → Customer
- Поля: _customer, _rating, _comment
- Методы: get_customer, get_rating, get_comment, edit_comment

ReviewManager 1 2 → Review
- Поля: reviews
- Методы: add_review, get_average_rating

### Ресторан (Restaurant)
Apron 4 6
- Поля: _size, _color, _assigned_to, _is_clean
- Методы: assign_to, unassign, mark_dirty, wash, is_clean, get_info

ChildMenu 2 3 → Menu
- Поля: _colour, _with_coloring_book
- Методы: ask_for_coloring_book, get_colour, with_coloring_book

CutlerySet 3 3
- Поля: _set_id, _pieces, _in_stock
- Методы: take_set, return_set, get_stock

HighChair 2 4
- Поля: _chair_id, _status
- Методы: occupy, release, mark_broken, get_status

MaintenanceRequest 3 4
- Поля: _equipment, _description, _fixed
- Методы: get_equipment, get_description, is_fixed, mark_fixed

Menu 1 3 → MenuItem
- Поля: _items
- Методы: add_item, remove_item, find_item

MenuItem 3 4
- Поля: _name, _price, _description
- Методы: get_name, get_price, get_description, update_price

MusicPlaylist 3 4
- Поля: _name, _tracks, _current
- Методы: add_track, next_track, get_current, get_info

Reservation 4 6 → Customer, Table
- Поля: _customer, _table, _time, _confirmed
- Методы: get_customer, get_table, get_time, is_confirmed, confirm, cancel

Table 3 4
- Поля: _number, _seats, _reserved
- Методы: get_number, is_reserved, reserve, free_table

TableMenuQRCode 3 5
- Поля: _table_number, _code, _active
- Методы: deactivate, activate, is_active, get_code, get_table

ToySet 3 3
- Поля: _toy_id, _description, _in_stock
- Методы: checkout, return_toy, get_stock

### Поставки (Supply)
Supplier 3 4 → Ingredient
- Поля: _name, _contact, _products
- Методы: get_name, get_contact, get_products, place_order

SupplyOrder 3 4 → Supplier, Ingredient
- Поля: _supplier, _items, _status
- Методы: get_supplier, get_items, get_status, mark_received

### Утилиты (Utils)
CleaningSchedule 3 4
- Поля: _area, _frequency, _last_done
- Методы: get_area, get_frequency, get_last_done, mark_done

PizzaBuilder 1 3 → Ingredient
- Поля: ingredients
- Методы: add_base, add_topping, build

Schedule 2 3 → Employee
- Поля: _employee, _shifts
- Методы: get_employee, get_shifts, add_shift

TimeTracker 2 1 → Employee
- Поля: employee, hours_worked
- Методы: add_hours
