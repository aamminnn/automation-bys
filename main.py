import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QCheckBox, QPlainTextEdit
from PyQt5.QtGui import QFont
import ui_run as ui
from prettytable import PrettyTable

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Automation Script')

        """
        WIDGET
        """
        font = QFont("Arial", 30)
        title = QLabel(self)
        title.setText('AUTOMATION SCRIPT')
        title.move(100,20)
        title.setFont(font)

        self.instance = QLineEdit(self)
        self.instance.setMaxLength(100)
        self.instance.setPlaceholderText("Instance URL")
        self.instance.setFixedWidth(500)

        self.password = QLineEdit(self)
        self.password.setMaxLength(100)
        self.password.setPlaceholderText("Instance Password")
        self.password.setFixedWidth(500)

        self.checked_checkbox = []  # selected testcase
        
        self.checkbox_1 = QCheckBox("OrganizationBasicData", self)
        self.checkbox_1.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'OrganizationBasicData'))

        self.checkbox_2 = QCheckBox("RepoData", self)
        self.checkbox_2.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'RepoData'))

        self.checkbox_3 = QCheckBox("SampleBranch", self)
        self.checkbox_3.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'SampleBranch'))

        self.checkbox_4 = QCheckBox("PullRequest", self)
        self.checkbox_4.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'PullRequest'))

        self.checkbox_5 = QCheckBox("Release", self)
        self.checkbox_5.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'Release'))

        self.checkbox_6 = QCheckBox("Issue", self)
        self.checkbox_6.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'Issue'))

        self.checkbox_7 = QCheckBox("Project", self)
        self.checkbox_7.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'Project'))

        self.checkbox_8 = QCheckBox("Wiki", self)
        self.checkbox_8.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'Wiki'))

        self.checkbox_9 = QCheckBox("Webhook", self)
        self.checkbox_9.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'Webhook'))

        self.checkbox_10 = QCheckBox("PreReceiveHook", self)
        self.checkbox_10.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'PreReceiveHook'))

        self.checkbox_11 = QCheckBox("Gist", self)
        self.checkbox_11.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'Gist'))

        self.checkbox_12 = QCheckBox("RepoPages", self)
        self.checkbox_12.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'RepoPages'))

        self.checkbox_13 = QCheckBox("OrganizationPackages", self)
        self.checkbox_13.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'OrganizationPackages'))

        self.checkbox_14 = QCheckBox("OrganizationPackages2", self)
        self.checkbox_14.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'OrganizationPackages2'))

        self.checkbox_15 = QCheckBox("RepoPackage", self)
        self.checkbox_15.stateChanged.connect(lambda state: self.checkbox_state_changed(state, 'RepoPackage'))

        self.checkbox_x = QCheckBox("Select All", self)
        self.checkbox_x.stateChanged.connect(lambda state: self.select_all_checkboxes(state))

        self.all_checkbox = [self.checkbox_1, self.checkbox_2, self.checkbox_3, self.checkbox_4, 
                             self.checkbox_5, self.checkbox_6, self.checkbox_7, self.checkbox_8,
                             self.checkbox_9, self.checkbox_10, self.checkbox_11,self.checkbox_12,
                             self.checkbox_13,self.checkbox_14,self.checkbox_15] # all testcase

        self.button_run = QPushButton('Run',self)
        self.button_run.clicked.connect(lambda: self.perform_operation('Run'))

        self.button_verify = QPushButton('Verify',self)
        self.button_verify.clicked.connect(lambda: self.perform_operation('Verify'))

        self.output_text_edit = QPlainTextEdit(self)

        """
        LAYOUT
        """
        # Create a layout and add the QLineEdit widget to it
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.instance)
        layout.addWidget(self.password)

        """Left column of testcase"""
        layout_tc_v1 = QVBoxLayout(self)
        layout_tc_v1.addWidget(self.checkbox_1)
        layout_tc_v1.addWidget(self.checkbox_2)
        layout_tc_v1.addWidget(self.checkbox_3)
        layout_tc_v1.addWidget(self.checkbox_4)
        layout_tc_v1.addWidget(self.checkbox_5)
        layout_tc_v1.addWidget(self.checkbox_6)
        layout_tc_v1.addWidget(self.checkbox_7)
        layout_tc_v1.addWidget(self.checkbox_x)

        """Right column of testcase"""
        layout_tc_v2 = QVBoxLayout(self)
        layout_tc_v2.addWidget(self.checkbox_8)
        layout_tc_v2.addWidget(self.checkbox_9)
        layout_tc_v2.addWidget(self.checkbox_10)
        layout_tc_v2.addWidget(self.checkbox_11)
        layout_tc_v2.addWidget(self.checkbox_12)
        layout_tc_v2.addWidget(self.checkbox_13)
        layout_tc_v2.addWidget(self.checkbox_14)
        layout_tc_v2.addWidget(self.checkbox_15)

        """add left and right column together"""
        layout_tc_h = QHBoxLayout(self)
        layout_tc_h.addLayout(layout_tc_v1)
        layout_tc_h.addLayout(layout_tc_v2)

        """Show testcase column"""
        layout.addLayout(layout_tc_h)

        """Add button side by side"""
        layout_h = QHBoxLayout(self)
        layout_h.addWidget(self.button_run)
        layout_h.addWidget(self.button_verify)

        """Display output field"""
        layout.addWidget(self.output_text_edit)

        # Set the layout for the main window
        self.setLayout(layout)
        layout.addLayout(layout_h)
        self.show()

    """
    FUNCTIONS
    """
    def perform_operation(self, button_name):
        print(self.checked_checkbox)
        if self.checked_checkbox:
            url = self.instance.text()
            password = self.password.text()
            if button_name == 'Run':
                verify = False
            else:
                verify = True
            # Add your logic here based on the selected checkbox and button
            version, oper, ver, tab = ui.run(url, password, verify, self.checked_checkbox)
            self.output_text_edit.appendPlainText(f'Instance Url: {url}')
            self.output_text_edit.appendPlainText(f'Instance Password: {password}')
            self.output_text_edit.appendPlainText(f'Instance Version: {version}')

            self.output_text_edit.appendPlainText(f'\n------------DATA OPERATION SUMMARY-------------')
            for i in oper:
                self.output_text_edit.appendPlainText(i)

            self.output_text_edit.appendPlainText(f'\n------------DATA VERIFICATION SUMMARY-------------')
            for j in ver:
                self.output_text_edit.appendPlainText(j)
            
            self.output_text_edit.appendPlainText(f'\n------------TESTCASE SUMMARY-------------')
            tab_string = tab.get_string()
            self.output_text_edit.appendPlainText(tab_string)
        else:
            print(f"No checkbox selected for {button_name} operation.")

    def checkbox_state_changed(self, state, checkbox_name):
        if state == 2:  # 2 corresponds to Checked state
            if checkbox_name not in self.checked_checkbox:
                self.checked_checkbox.append(checkbox_name)
        else:
            if checkbox_name in self.checked_checkbox:
                self.checked_checkbox.remove(checkbox_name)

    def select_all_checkboxes(self, state):
        for checkbox in self.all_checkbox:
            checkbox.setChecked(state == 2)
            if state == 2:
                if checkbox.text() not in self.checked_checkbox:
                    self.checked_checkbox.append(checkbox.text())
            else:
                if checkbox.text() in self.checked_checkbox:
                    self.checked_checkbox.remove(checkbox.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
