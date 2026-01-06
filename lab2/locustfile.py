from locust import HttpUser, task
class QuickstartUser(HttpUser):
    @task
    def test_integral(self):
        self.client.get("/integral/0/3.14159")