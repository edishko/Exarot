# ____ ____ ____ ____ # Libaries 
import requests
import os
import sys
from exaroton import Exaroton
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# ____ ____ ____ ____ # Classes

class App(QWidget):

    # ____ ____ ____ # Helpers #
    def FUNC_DATA(self, database):
        
        if not os.path.exists(database): # Check if the file exists
            with open(database, 'w') as file: # Create an empty file if it doesn't exist
                pass

        with open(database, 'r') as file: # Read the file and return the data
            return [line.strip() for line in file.readlines() if line.strip() != '' and line.strip() is not None]

    def FUNC_WIDGET_ADD(self, widget, grid):
        # Create widget variables #
        widget_instance = widget()
        self.layout.addWidget(widget_instance, grid[0], grid[1])

        return widget_instance
    
    def FUNC_WIDGET_START(self, token):

        credit = max([account[1]['credits'] for account in self.DICTIONARY['ACCOUNTS']])

        for account in self.DICTIONARY['ACCOUNTS']:
            if account[1]['credits'] == credit:
                self.FUNC_REQUEST_START(account[0])

    def FUNC_REQUEST_START(self, token):

        url = f"https://api.exaroton.com/v1/servers/{'XiPTrDvCv1M2WOUp'}/start/"
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "useOwnCredits": True
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("Server started successfully.")
        else:
            print("Failed to start server.")

        # After the `response = requests.post(url, headers=headers, json=payload)` line
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())

    # ____ ____ ____ # Main #
    def __init__(self):
        super().__init__() # Call super-class #
        self.layout = QGridLayout() # App layout #
        self.setWindowTitle("exarot")

        self.DICTIONARY = \
        {
            'DATABASE': 'db.txt',
        }
        self.DICTIONARY['TOKENS'] = self.FUNC_DATA(self.DICTIONARY['DATABASE'])
        self.DICTIONARY['ACCOUNTS'] = [(token, vars(Exaroton(token).get_account())) for token in self.DICTIONARY['TOKENS']]

        self.UI()
    
    def UI(self):

        START_BUTTON = self.FUNC_WIDGET_ADD(lambda: QPushButton('\n' + 'Start Server' + '\n'), (0,0))
        START_BUTTON.clicked.connect(self.FUNC_WIDGET_START)
        
        def UPDATE_STATS():
            for index, account in enumerate(self.DICTIONARY['ACCOUNTS']):
                self.FUNC_WIDGET_ADD(lambda: QLabel(account[1]['name'] + ': ' + str(account[1]['credits'])), (index + 1, 0))
        
        UPDATE_STATS()
        START_BUTTON.clicked.connect(UPDATE_STATS)    
        
        # Add layout to app window
        self.setLayout(self.layout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Roboto", 15)  # Set the desired font and size
    app.setFont(font)

    ex = App()
    ex.show()
    sys.exit(app.exec_())
