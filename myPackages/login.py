import yaml


class guard:
    def __init__(self, loginConfigPath):
        # Load configration
        with open(loginConfigPath, "r", encoding="utf-8") as f:
            self.lableConfig = yaml.safe_load(f)
        self.userNameList = self.lableConfig["usernames"]
        self.password = self.lableConfig["password"]

    def login(self, username, password):
        if username not in self.userNameList:
            return "[Error]: Tên đăng nhập ko đúng ❌"
        if password != self.password:
            return "[Error]: Mật khẩu không đúng ❌"
        return "[Success]"