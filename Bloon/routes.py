class RouteManager:
    def __init__(self):
        self.app_names, self.routes, self.function = [], [], []
        self.namespace = {}

    def validate(self):
        if not self.app_names and not self.routes and not self.function:
            return True
        return len(self.app_names) + len(self.routes) + len(self.function) % 3 == 0

    def check_empty(self):
        return len(self.app_names) + len(self.routes) + len(self.function) == 0

    def register(self, value, as_parent: bool = False, key: str = "", app_name: str = ""):
        if as_parent:
            self.namespace.update({key: Node(parent=True, value=value if value != {} else {})})
        else:
            self.app_names.append(app_name)
            self.routes.append(key)
            self.function.append(value)

    def get_node(self, route: str = None, app_name: str = None):
        if route is None and app_name is None:
            raise TypeError("You must provide route or app_name in order to get node.")

        r = self.routes
        if app_name is not None:
            r = self.app_names

        try:
            return self.function[r.index(route or app_name)]
        except ValueError:
            return None


class Node:
    def __init__(self, value, parent: bool = False):
        self.parent = parent

        if self.parent:
            if type(value) == dict:
                raise TypeError("Node must be a child if parent is set to True.")
            self.nodes = {**value}
        else:
            self.value = value

    def get_child(self, key: str = None):
        if not self.parent:
            return self.value
        else:
            return self.nodes.get(key)
