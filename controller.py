from testcase import testcase3_7,testcase3_8,testcase3_9,testcase3_10,testcase3_11,testcase3_12,testcase3_13,testcase3_14,testcase3_15
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
import time, os
import version as v
import index as cd
import re

is_fail = '\033[91mFAIL\033[0m'  # 91 is the ANSI code for red
is_stop = '\033[91mSTOPPED\033[0m'  # 91 is the ANSI code for red
is_pass = '\033[92mPASS\033[0m'  # 92 is the ANSI code for green
is_complete = '\033[92mCOMPLETED\033[0m'  # 92 is the ANSI code for green


class Controller:
    def __init__(self, url):
        self.url = url
        # self.driver = None

    def chromedriver(self):
        api = cd.get_api()
        cd.extract_chromedriver(api)

    def open_chrome(self):
        # path_to_chrome_driver = r'./chromedriver-mac-x64-v126/chromedriver'
        # service = Service(executable_path=path_to_chrome_driver)

        # with webdriver.Chrome(service=service) as self.driver:
        # self.driver = webdriver.Chrome(service=service)
        self.driver = webdriver.Chrome()

        # Get the capabilities
        capabilities = self.driver.capabilities

        # Check the version of Chrome Browser
        chrome_version_string = capabilities['chrome']['chromedriverVersion']
        chrome_version = re.search(r'^(\d+)', chrome_version_string).group(1)
        print("Chrome version:", chrome_version)
        time.sleep(1)
    
    def sign_in(self, username, password):
        self.driver.get(f'{self.url}/login')
        unsecured = False
        try:
            self.driver.find_element(By.ID,'details-button')
            print("Site is Unsecured (HTTP)")
            unsecured = True
        except Exception as e:
            print(f'Site is Secured (HTTPS)')

        if unsecured:
            advanced = self.driver.find_element(By.ID, 'details-button')
            advanced.click()
            proceed = self.driver.find_element(By.ID, 'proceed-link')
            proceed.click()
            time.sleep(2)

        self.driver.find_element("id","login_field").send_keys(username)
        self.driver.find_element("id","password").send_keys(password)
        self.driver.find_element("name","commit").click()
        time.sleep(3)

    def get_version(self):
        version = self.driver.find_element(By.CSS_SELECTOR, '.current-branch.css-truncate.expandable .current-branch-name.css-truncate-target').text
        print(version)
        return version

    def execute_testcase(self, version, opt:list, verify_data):
        verify_message_summary = []
        operation_summary = []
        table_testcase = []
        table_result = []
        version = version #version
        # operations = testcase
        if v.version_list_3_7 in version:
            operations = testcase3_7
            print(f'Running Script on v3_7.py')
        elif v.version_list_3_8 in version:
            operations = testcase3_8
            print(f'Running Script on v3_8.py')
        elif v.version_list_3_9 in version:
            operations = testcase3_9
            print(f'Running Script on v3_9.py')
        elif v.version_list_3_10 in version:
            operations = testcase3_10
            print(f'Running Script on v3_10.py')
        elif v.version_list_3_11 in version:
            operations = testcase3_11
            print(f'Running Script on v3_11.py')
        elif v.version_list_3_12 in version:
            operations = testcase3_12
            print(f'Running Script on v3_12.py')
        elif v.version_list_3_13 in version:
            operations = testcase3_13
            print(f'Running Script on v3_13.py')
        elif v.version_list_3_14 in version:
            operations = testcase3_14
            print(f'Running Script on v3_14.py')
        elif v.version_list_3_15 in version:
            operations = testcase3_15
            print(f'Running Script on v3_15.py')
        if opt == None:
            # Run all processes in operations
            for op in operations:
                c = op()
                print("\n---------STARTING NEW TESTCASE-----------")
                try:
                    print(f'Running {c.__class__.__name__} testcase')
                    version,operation_message,verify_message = c.run(self.driver, self.url, version, verify_data)
                    status = is_pass
                except Exception as e:
                    print(f'{c.__class__.__name__} failed to execute. {e}')
                    operation_message = f'Operation {c.__class__.__name__} - {is_stop}'
                    verify_message = f'Verification {c.__class__.__name__} Data - {is_stop}.'
                    status = is_fail
                operation_summary.append(operation_message)
                verify_message_summary.append(verify_message)
                table_testcase.append(c.__class__.__name__)
                table_result.append(status)
                print("---------END OF TESTCASE-----------\n")
        else:
            for item in opt:
                print("\n---------STARTING NEW TESTCASE-----------")
                for op in operations:
                    c = op()
                    if item == c.__class__.__name__:
                        try:
                            print(f'Running {c.__class__.__name__} testcase')
                            version,operation_message,verify_message = c.run(self.driver, self.url, version, verify_data)
                            status = is_pass
                        except Exception as e:
                            print(f'{c.__class__.__name__} failed to execute. {e}')
                            operation_message = f'Operation {c.__class__.__name__} - {is_stop}'
                            verify_message = f'Verification {c.__class__.__name__} Data - {is_stop}.'
                            status = is_fail
                        operation_summary.append(operation_message)
                        verify_message_summary.append(verify_message)
                        table_testcase.append(c.__class__.__name__)
                        table_result.append(status)
                        print("---------END OF TESTCASE-----------\n")
                        break
                    else:
                        continue
                else:
                    print(f"Operation not found for item: {item}")
                    print("---------END OF TESTCASE-----------\n")
        return version,operation_summary, verify_message_summary, table_testcase, table_result
    
    def instance_summary(self,version):
        print(f'instance = {self.url}')
        print(f'instance version = {version}')
    
    def testcase_summary(self, summary:list):
        for item in summary:
            print(f'{item}')

    def verification_summary(self, v_summary:list):
        for item in v_summary:
            print(item)

    def quit_chrome(self):
        if self.driver:
            self.driver.quit()

