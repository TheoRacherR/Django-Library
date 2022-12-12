from rolepermissions.roles import AbstractUserRole

class Customer(AbstractUserRole):
    available_permissions = {
        'customer': True,
        'bookseller': False,
        'admin': False,
    }

class Bookseller(AbstractUserRole):
    available_permissions = {
        'customer': True,
        'bookseller': True,
        'admin': False,

    }

class Admin(AbstractUserRole):
    available_permissions = {
        'customer': True,
        'bookseller': True,
        'admin': True,
    }