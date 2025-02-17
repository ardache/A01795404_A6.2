"""Hotel Reservation System

This module implements a hotel reservation system with functionality
for managing hotels, customers, and reservations using file-based
persistence.
"""

import json
import os
import unittest
from typing import List, Dict

HOTEL_FILE = "hotels.json"
CUSTOMER_FILE = "customers.json"
RESERVATION_FILE = "reservations.json"
TEST_DATA_FILE = "test_data.json"


def load_data(file_path: str) -> List[Dict]:
    """Load data from a JSON file. If file is missing or invalid, return []."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print(f"Warning: Invalid format in {file_path}. Expected a list.")
            return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading {file_path}: {e}. Resetting data.")
        return []


def save_data(file_path: str, data: List[Dict]) -> None:
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_test_data():
    """Load test data from a JSON file, handling errors gracefully."""
    try:
        with open(TEST_DATA_FILE, 'r', encoding="utf-8") as file:
            test_data = json.load(file)
            if not isinstance(test_data, dict):
                raise ValueError("Invalid test data format.")
            return {
                "hotels": test_data.get("hotels", []),
                "customers": test_data.get("customers", []),
                "reservations": test_data.get("reservations", [])
            }
    except (json.JSONDecodeError, IOError, ValueError) as e:
        print(f"Error al cargar archivo: {e}. Using empty defaults.")
        return {"hotels": [], "customers": [], "reservations": []}


class Hotel:
    """Represents a hotel with a name, location, and rooms."""
    def __init__(self, name: str, location: str, rooms: int):
        self.name = name
        self.location = location
        self.rooms = rooms
        self.available_rooms = rooms

    def to_dict(self) -> Dict:
        """Convert the Hotel instance into a dictionary."""
        return self.__dict__

    @staticmethod
    def create_hotel(name: str, location: str, rooms: int):
        """Create and store a new hotel."""
        hotels = load_data(HOTEL_FILE)
        hotels.append(Hotel(name, location, rooms).to_dict())
        save_data(HOTEL_FILE, hotels)

    @staticmethod
    def delete_hotel(name: str):
        """Delete a hotel by name."""
        hotels = [h for h in load_data(HOTEL_FILE) if h['name'] != name]
        save_data(HOTEL_FILE, hotels)

    @staticmethod
    def get_hotel(name: str) -> Dict:
        """Retrieve a hotel by name."""
        for hotel in load_data(HOTEL_FILE):
            if hotel['name'] == name:
                return hotel
        return {}


class Customer:
    """Represents a customer with a name and email."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def to_dict(self) -> Dict:
        """Convert the Customer instance into a dictionary."""
        return self.__dict__

    @staticmethod
    def create_customer(name: str, email: str):
        """Create and store a new customer."""
        customers = load_data(CUSTOMER_FILE)
        customers.append(Customer(name, email).to_dict())
        save_data(CUSTOMER_FILE, customers)

    @staticmethod
    def delete_customer(name: str):
        """Delete a customer by name."""
        customers = [c for c in load_data(CUSTOMER_FILE) if c['name'] != name]
        save_data(CUSTOMER_FILE, customers)

    @staticmethod
    def get_customer(name: str) -> Dict:
        """Retrieve a customer by name."""
        for customer in load_data(CUSTOMER_FILE):
            if customer['name'] == name:
                return customer
        return {}


class Reservation:
    """Handles reservations between customers and hotels."""

    def __init__(self, customer: str, hotel: str):
        self.customer = customer
        self.hotel = hotel

    def to_dict(self) -> Dict:
        """Convert the Reservation instance into a dictionary."""
        return self.__dict__

    @staticmethod
    def create_reservation(customer: str, hotel: str):
        """Create and store a new reservation."""
        reservations = load_data(RESERVATION_FILE)
        reservations.append(Reservation(customer, hotel).to_dict())
        save_data(RESERVATION_FILE, reservations)

    @staticmethod
    def cancel_reservation(customer: str, hotel: str):
        """Cancel a reservation."""
        reservations = [
            r for r in load_data(RESERVATION_FILE)
            if not (r['customer'] == customer and r['hotel'] == hotel)
        ]
        save_data(RESERVATION_FILE, reservations)

    @staticmethod
    def get_reservations() -> List[Dict]:
        """Retrieve all reservations."""
        return load_data(RESERVATION_FILE)


class TestHotelSystem(unittest.TestCase):
    """Unit tests for the hotel reservation system."""
    def setUp(self):
        """Load test data from a JSON file before each test."""
        test_data = load_test_data()
        save_data(HOTEL_FILE, test_data["hotels"])
        save_data(CUSTOMER_FILE, test_data["customers"])
        save_data(RESERVATION_FILE, test_data["reservations"])

    def test_create_hotel(self):
        """Test hotel creation."""
        Hotel.create_hotel("Hotel Pucon", "Chile", 15)
        self.assertEqual(len(load_data(HOTEL_FILE)), 3)

    def test_create_customer(self):
        """Test customer creation."""
        Customer.create_customer("Ardash Hdez", "Hotel Pucon")
        self.assertEqual(len(load_data(CUSTOMER_FILE)), 3)

    def test_create_reservation(self):
        """Test reservation creation."""
        Reservation.create_reservation("Ardash Hdez", "Hotel Ankor Wat")
        self.assertEqual(len(load_data(RESERVATION_FILE)), 3)

    def test_cancel_reservation(self):
        """Test reservation cancellation."""
        Reservation.cancel_reservation("Pryha Terima", "Hotel Ankor Wat")
        self.assertEqual(len(load_data(RESERVATION_FILE)), 1)


if __name__ == "__main__":
    unittest.main()
