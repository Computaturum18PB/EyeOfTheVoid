from PySide6.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QLabel, QRadioButton, QLineEdit, QMessageBox
from utils.crypto_master import cm

class ChoicePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome")
        self.setSubTitle("Choose action")
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("What do you want doing?"))
        
        self.register_radio = QRadioButton("Register")
        self.login_radio = QRadioButton("Login in exists account")
        self.register_radio.setChecked(True)
        
        layout.addWidget(self.register_radio)
        layout.addWidget(self.login_radio)
        
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
    
    def validatePage(self):
        username = self.username.text()
        password = self.password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Fill all fields!")
            return False
        
        if cm.check_password(username, password):
            return True
        else:
            QMessageBox.warning(self, "Login error", "Invalid username or password!")
            return False

class RegisterPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Register")
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
    
    def validatePage(self):
        username = self.username.text()
        password = self.password.text()
        confirm = self.confirm.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Fill all fields!")
            return False
        
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return False
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters!")
            return False
        
        if cm.create_user(username, password):
            QMessageBox.information(self, "Success", f"User '{username}' created successfully!")
            return True
        else:
            QMessageBox.warning(self, "Error", f"User '{username}' already exists!")
            return False

class ProtectorWindow(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authorization")
        self.setWizardStyle(QWizard.ModernStyle)  

        self.choice_page = ChoicePage()
        self.register_page = RegisterPage()
        self.login_page = LoginPage()

        self.addPage(self.choice_page)
        self.addPage(self.register_page)
        self.addPage(self.login_page)
    
    def nextId(self):
        current_id = self.currentId()
        
        if current_id == 0:
            is_login = self.field("action")
            if is_login:
                return 2
            else:
                return 1 
        
        if current_id == 1:
            return 2
        
        return super().nextId()
    
    def reject(self):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to cancel?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            super().reject()