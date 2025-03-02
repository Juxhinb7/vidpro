from app.component.decorator.singleton import singleton


@singleton()
class UserController:
    def get_users(self):
        return "Hello"


user_controller = UserController()