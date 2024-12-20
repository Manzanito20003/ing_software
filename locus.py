from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def happy_path(self):
        self.client.get("/happy-path")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)