from enum import Enum


class UserRole(Enum):
    ADMIN = "Admin"
    DRIVER = "Driver"
    PASSENGER = "Passenger"

    @classmethod
    def choices(cls):
        return [(role.value, role.value) for role in cls]


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        return [(gender.value, gender.value) for gender in cls]


class TransactionType(Enum):
    RECHARGE = "Recharge"
    TRANSFER = "Transfer"
    PAYMENT = "Payment"

    @classmethod
    def choices(cls):
        return [(transaction.value, transaction.value) for transaction in cls]


class BookingStatus(Enum):
    PAID = "Paid"
    CANCELLED = "Cancelled"
    COMPLETE = "Complete"
    PENDING = "Pending Payment"

    @classmethod
    def choices(cls):
        return [(status.value, status.value) for status in cls]
