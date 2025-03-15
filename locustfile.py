from locust import HttpUser, task, between

class BusBookingUser(HttpUser):
    """
    Simulates user behavior on the bus booking system.
    """
    wait_time = between(1, 3)  # Wait time between tasks (simulating real users)

    @task(2)
    def search_buses(self):
        """Simulate searching for available buses."""
        self.client.get("/matatus/buses/")

