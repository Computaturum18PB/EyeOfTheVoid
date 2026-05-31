from PySide6.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QLabel, QRadioButton, QLineEdit

class ChoicePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome")
        self.setSubTitle("Choose action")
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("What do you want doing?"))
        
        self.login_radio = QRadioButton("Login in exists account")
        self.register_radio = QRadioButton("Register")
        self.login_radio.setChecked(True)
        
        layout.addWidget(self.login_radio)
        layout.addWidget(self.register_radio)
        
        self.setLayout(layout)

        self.registerField("action", self.login_radio, "checked")

class LoginPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Account login")
        self.setSubTitle("Enter your data")
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Login:"))
        self.username = QLineEdit()
        layout.addWidget(self.username)
        
        layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        self.setLayout(layout)
        
        self.registerField("login_username", self.username)
        self.registerField("login_password", self.password)

class RegisterPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Regiseter")
        self.setSubTitle("Create new account")
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Login:"))
        self.username = QLineEdit()
        layout.addWidget(self.username)
        
        layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        layout.addWidget(QLabel("Confirm password:"))
        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm)
        
        self.setLayout(layout)
        
        self.registerField("register_username", self.username)
        self.registerField("register_password", self.password)

class ProtectorWindow(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authorization")
        self.setWizardStyle(QWizard.ModernStyle)        

        self.choice_page = ChoicePage()
        self.login_page = LoginPage()
        self.register_page = RegisterPage()

        self.addPage(self.choice_page)
        self.addPage(self.login_page) 
        self.addPage(self.register_page)
    
    def nextId(self):
        current_id = self.currentId()
        
        if current_id == 0:
            is_login = self.field("action")
            if is_login:
                return 1 
            else:
                return 2 
        
        return super().nextId()
    
    def accept(self):
        is_login = self.field("action")
        
        if is_login:
            username = self.field("login_username")
            password = self.field("login_password")
        else:
            username = self.field("register_username")
            password = self.field("register_password")
        
        super().accept()