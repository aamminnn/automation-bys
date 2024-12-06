from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from counter import counter 
import time, os
import configparser
import version as v
import random,json

"""
VARIABLES
"""
is_fail = '\033[91mFailed\033[0m'  # 91 is the ANSI code for red
is_pass = '\033[92mPassed\033[0m'  # 92 is the ANSI code for green
is_complete = '\033[92mComplete\033[0m'  # 92 is the ANSI code for green
is_incomplete = '\033[91mIncomplete\033[0m'  # 91 is the ANSI code for red
is_skip = '\033[92mSkipped\033[0m'  # 92 is the ANSI code for green
rand = random.randint(10, 99)
basic_org = f'org{rand}'
alert_org = f'alert-org{rand}'
# Read the JSON file
with open('naming.json', 'r') as file:
    name = json.load(file)

"""
HELPER FUNCTION
"""
def checkpoint(message:str) -> None:
    print(f'\033[33m{message}\033[0m') #yellow

def load_config():
    config = configparser.ConfigParser()
    with open("config.ini","r") as file_object:
        config.read_file(file_object)
    return config

"""
TESTCASE OPERATION
"""
class PersonalAccessToken:
    def run(self, driver, url, version, verify_data):
        checkpoint(f'STARTING {__class__.__name__} OPERATION')
        if verify_data == False: #form-group errored
            driver.get(f'{url}/settings/tokens/new')
            time.sleep(2)
            pat = driver.find_element(By.ID, 'oauth_access_description').send_keys('pat_auto')
            tick_repo = driver.find_element(By.CSS_SELECTOR, '.js-checkbox-scope.parent-checkbox-scope')
            if tick_repo.text == "repo":
                tick_repo.click()
            generate_token = driver.find_element(By.CSS_SELECTOR, '.new_oauth_access .btn-primary.btn').click()
            time.sleep(2)
            try:
                driver.find_element(By.CSS_SELECTOR,'.form-group.errored')
                print('pat_auto already existed')
                op_message = f'\'pat_auto\' already exist - {is_skip}'
            except:
                token = driver.find_element(By.ID, 'new-oauth-token')
                token_value = token.text
                with open('./ignore/pat.txt', 'a') as file: 
                    file.write(str(f'{url} - {token_value}\n')) 
                print("Personal Access Token \'pat_auto\' created")
                op_message = f'Personal Access Token \'pat_auto\' created - {is_pass}'
            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}'
        checkpoint(f'OPERATION {__class__.__name__} COMPLETED')

        checkpoint("VERIFYING PERSONAL ACCESS TOKEN DATA")
        pat_exist = 'pat_auto'
        try:
            driver.get(f'{url}/settings/tokens')
            time.sleep(2)
            pat_list = driver.find_element(By.CSS_SELECTOR, '.listgroup-item .token-description a')
            pat_value = pat_list.text
            if pat_value == pat_exist:
                print(f"Personal Token {pat_exist} already existed")
                verify_status = True
                message1 = f"Personal Token {pat_exist} already existed - {is_pass}"
            else:
                print(f"Personal Access Token is not {pat_exist}. Creating new Personal Access Token")
                create_pat = True
                verify_status = False
                message2 = f"Personal Access Token is not {pat_exist} - {is_fail}"
            
        except Exception as e:
            print("Personal access token missing. Creating new Personal Access Token.")
            verify_status = False
            message2 = f"Personal access token missing - {is_fail}"
        checkpoint("PERSONAL ACCESS TOKEN DATA VERIFICATION COMPLETED")

        if verify_status:
            v_message = f'{__class__.__name__} Data - {is_complete}'
            verify_message = f'{v_message} \n  {message1}'
        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete} \n  {message2}'
        
        return version, operation_message, verify_message

class OrganizationBasicData:
    def run(self, driver, url, version, verify_data):
        checkpoint(f'Operation {__class__.__name__}')
        if verify_data == False:
            driver.get(f'{url}/organizations/new')
            driver.find_element(By.CSS_SELECTOR, '.form-control.js-new-organization-name.width-full.py-1').send_keys(basic_org)
            driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
            op_message = f'Organization \'{name['OrganizationBasic']}\' created - {is_pass}'
            name['OrganizationBasic'] = basic_org
            with open('naming.json', 'w') as file:
                json.dump(name, file, indent=4)
            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}'
        print(operation_message)

        checkpoint(f'Verification {__class__.__name__}')
        driver.get(f'{url}')
        driver.get(f'{url}/{name['OrganizationBasic']}')
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            verify_status = False
        except:
            verify_status = True

        if verify_status:
            verify_message = f'{__class__.__name__} Data - {is_complete}. \n  Org \'{name['OrganizationBasic']}\' found - {is_pass}'
        else:
            verify_message = f'{__class__.__name__} Data - {is_fail}. Org \'{name['OrganizationBasic']}\' not found.'

        print(verify_message)

        return version, operation_message, verify_message

class RepoData:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            checkpoint(f'Operation {__class__.__name__}')
            if verify_data == False:
                operation = True
                #create repo code-scanning 
                driver.get(f'{url}/organizations/{name['OrganizationBasic']}/repositories/new')
                driver.find_element(By.ID,'repository_name').send_keys('data')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.form-control.js-repo-name.js-repo-name-auto-check.short.is-autocheck-errored')
                    op_message = f'repo \'data\' already existed - {is_pass}'
                except:
                    driver.find_element(By.ID,'repository_auto_init').click()
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.js-with-permission-fields .btn-primary.btn').click()
                    time.sleep(3)
                    op_message = f'Repo \'data\' created. Please create runner manually - {is_pass}'
            else:
                operation = False

            if operation:
                operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
            else:
                operation_message = f'{__class__.__name__} Data - {is_skip}'
            print(operation_message)

            checkpoint(f'Verification {__class__.__name__}')
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually - {is_fail}'
                verify_status = False
            except:
                verify_status = True
   
            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message}. Repo \'data\' found!'
            else:
                verify_message = f'{__class__.__name__} Data - {is_incomplete}. \n  {message}'

        else:
            verify_message = f'Verification {__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'Operation {__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)

        print(verify_message)
        return version, operation_message, verify_message

class SampleBranch:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True
            
            if verify_status:
                checkpoint(f'Operation {__class__.__name__}')
                if verify_data == False: 
                    br_msg_ls = []
                    fl_msg_ls = []
                    sample_branch = ['sample-branch-1','sample-branch-2']
                    sample_branch_file = ['sample-branch-1-file.txt','sample-branch-2-file.txt']
                    x = random.randint(10, 50)
                    for i in range(2):
                        driver.get(f'{url}/{name['OrganizationBasic']}/data')
                        time.sleep(2)
                        #sample branch
                        branch_list = driver.find_element(By.CSS_SELECTOR, '.btn.css-truncate').click()
                        time.sleep(2)
                        branch_name = driver.find_element(By.ID, 'context-commitish-filter-field').send_keys(sample_branch[i])
                        time.sleep(2)
                        try:
                            #branch existed
                            branch_new = driver.find_element(By.CSS_SELECTOR, '.SelectMenu-item.wb-break-word').click()
                            op_br_message = f'New \'{sample_branch[i]}\' created - {is_pass}'
                        except:
                            driver.find_element(By.CSS_SELECTOR,'.d-flex.flex-column.flex-auto.overflow-auto .SelectMenu-list .SelectMenu-item').click()
                            op_br_message = f'\'{sample_branch[i]}\' already existed - {is_pass}'
                        br_msg_ls.append(op_br_message)
                        time.sleep(4)

                        #sample file
                        driver.get(f'{url}/{name['OrganizationBasic']}/data/tree/sample-branch-{i+1}')
                        time.sleep(2)
                        add_file = driver.find_element(By.CSS_SELECTOR, '.d-none.d-md-flex.flex-items-center').click()
                        create_new_file = driver.find_element(By.CSS_SELECTOR, '.dropdown-item.btn-link').click()
                        new_filename = driver.find_element(By.NAME, 'filename')
                        new_filename.send_keys(sample_branch_file[i])
                        file_content = driver.find_element(By.CLASS_NAME, 'CodeMirror-line')
                        file_content.send_keys("This is a sample file.")
                        submit_new_file = driver.find_element(By.ID, 'submit-file')
                        submit_new_file.click()
                        time.sleep(3)
                        try:
                            driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-error')
                            op_fl_message = f'\'{sample_branch_file[i]}\' already existed'
                        except:
                            op_fl_message = f'\'{sample_branch_file[i]}\' created - {is_pass}'
                        fl_msg_ls.append(op_fl_message)
                    op_br_message1 = br_msg_ls[0]
                    op_br_message2 = br_msg_ls[1]
                    op_fl_message1 = fl_msg_ls[0]
                    op_fl_message2 = fl_msg_ls[1]
                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete}\n  {op_br_message1}\n    {op_fl_message1}\n  {op_br_message2}\n    {op_fl_message2}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)

                checkpoint(f'Verification {__class__.__name__}')
                driver.get(f'{url}/{name['OrganizationBasic']}/data')
                time.sleep(4)   
                driver.find_element(By.CSS_SELECTOR, '.btn.css-truncate').click()
                time.sleep(2)
                sample_branch = ['sample-branch-1','sample-branch-2']
                br_message_ls = []
                for sample in sample_branch:
                    branch_list = driver.find_elements(By.CLASS_NAME,'SelectMenu-item')
                    for branch in branch_list:
                        if branch.text == sample:
                            br_message = f'{branch.text} found - {is_pass}'
                            br_message_ls.append(br_message)
                            break
                    else:
                        br_message = f'{branch.text} not found - {is_fail}'
                br_message1 = br_message_ls[0]
                br_message2 = br_message_ls[1]

                sample_fl = ['sample-branch-1-file.txt','sample-branch-2-file.txt']
                fl_message_list = []
                for i in range(2):
                    try:
                        driver.get(f'{url}/{name['OrganizationBasic']}/data/tree/sample-branch-{i+1}')
                        file_list = driver.find_elements(By.CSS_SELECTOR,'.Box-row.Box-row--focus-gray.py-2.d-flex.position-relative.js-navigation-item')
                        for file in file_list:
                            filename = file.find_element(By.CSS_SELECTOR, '.css-truncate.css-truncate-target.d-block.width-fit a')
                            if filename.text == sample_fl[i]:
                                fl_message = f'sample file found - {filename.text} - {is_pass}'
                                break
                        else:
                            fl_message = f'sample file not found - {is_fail}'
                    except:
                        fl_message = f'no sample-branch-{i+1} found'
                    fl_message_list.append(fl_message)
                fl_message1 = fl_message_list[0]
                fl_message2 = fl_message_list[1] 

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {br_message1}\n    {fl_message1}\n  {br_message2}\n    {fl_message2}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_incomplete}. {message}'
                operation_message = f'{__class__.__name__} Data - {is_incomplete}. \n  {message}'
                print(operation_message)

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)
        
        print(verify_message)
        
        return version, operation_message, verify_message

class SampleFile: #removed
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually - {is_fail}'
                verify_status = False
            except:
                verify_status = True

            if verify_status:
                checkpoint(f'Operation {__class__.__name__} ')
                if verify_data == False:
                    op_msg_ls = []
                    for i in range(1,3):  
                        add_file = driver.find_element(By.CSS_SELECTOR, '.d-none.d-md-flex.flex-items-center').click()
                        create_new_file = driver.find_element(By.CSS_SELECTOR, '.dropdown-item.btn-link').click()
                        new_filename = driver.find_element(By.NAME, 'filename').send_keys(f'sample-branch-{i}-file.txt')
                        file_content = driver.find_element(By.CLASS_NAME, 'CodeMirror-line').send_keys("This is a sample file.")
                        submit_new_file = driver.find_element(By.ID, 'submit-file').click()
                        time.sleep(3)
                        try:
                            driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-error')
                            op_message = f'\'sample-branch-{i}-file.txt\' already existed'
                        except:
                            op_message = f'\'sample-branch-{i}-file.txt\' created - {is_pass}'
                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)

                 
                #sample branch 1 file
                driver.find_element(By.CSS_SELECTOR, '.btn.css-truncate').click()
                time.sleep(2)
                #v3.7
                branch_list = driver.find_elements(By.CLASS_NAME,'SelectMenu-item')
                for branch in branch_list:
                    if branch.text == 'sample-branch-1':
                        branch.click()
                        branch_status = True
                        break
                else:
                    branch_status = False
                    message1 = f'{branch.text} not found - {is_fail}'
                if branch_status:
                    file_list = driver.find_elements(By.CSS_SELECTOR,'.css-truncate.css-truncate-target.d-block.width-fit')
                    for file in file_list:
                        if file.text == 'sample-branch-1-file.txt':
                            message1 = f'{file.text} found! - {is_pass}'
                            break
                        else:
                            continue
                    else:
                        message1 = f'{file.text} not found - {is_fail}'

                #sample branch 2 file
                driver.find_element(By.CSS_SELECTOR, '.btn.css-truncate').click()
                branch_list = driver.find_elements(By.CLASS_NAME,'SelectMenu-item')
                for branch in branch_list:
                    if branch.text == 'sample-branch-2':
                        branch.click()
                        branch_status = True
                        break
                else:
                    branch_status = False
                    message2 = f'{branch.text} not found - {is_fail}'
                if branch_status:
                    file_list = driver.find_elements(By.CSS_SELECTOR,'.css-truncate.css-truncate-target.d-block.width-fit')
                    for file in file_list:
                        if file.text == 'sample-branch-2-file.txt':
                            message2 = f'{file.text} found! - {is_pass}'
                            break
                        else:
                            continue
                    else:
                        message2 = f'{file.text} not found - {is_fail}'

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1} \n  {message2}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_incomplete}. \n  {message}'
                operation_message = f'{__class__.__name__} Data - {is_incomplete}. \n  {message}'
                print(operation_message)
        
        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)
        
        print(verify_message)
        
        return version, operation_message, verify_message

class PullRequest:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True
            
            if verify_status:
                checkpoint(f'Operation {__class__.__name__}')
                if verify_data == False: 
                    #closed pr
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/compare')
                    time.sleep(2)
                    pr_btn = driver.find_elements(By.CSS_SELECTOR,'.Button-label')
                    for elem in pr_btn:
                        if 'compare' in elem.text:
                            elem.click()
                            time.sleep(1)
                            branch_list = driver.find_elements(By.CLASS_NAME,'SelectMenu-item')
                            for branch in branch_list:
                                if branch.text == 'sample-branch-1':
                                    branch1_message = f'{branch.text} found - {is_pass}'
                                    branch.click()
                                    time.sleep(3)
                                    break
                            break
                    else:
                        branch1_message = f'sample-branch-1 not found - {is_fail}'
                    try:
                        #if branch 1 ada commit
                        driver.find_element(By.CSS_SELECTOR,'.js-details-target.btn-primary.btn').click()
                        time.sleep(2)
                        driver.find_element(By.ID,'pull_request_title').send_keys('Close Pull Request')
                        create_pr = driver.find_element(By.CSS_SELECTOR, '.hx_create-pr-button.js-sync-select-menu-button.btn-primary.btn.BtnGroup-item.flex-auto').click()
                        time.sleep(3)
                        merge_pr = driver.find_element(By.CSS_SELECTOR, '.merge-box-button.btn-group-merge.rounded-left-2.btn.btn-primary.BtnGroup-item.js-details-target.hx_create-pr-button').click()
                        time.sleep(3)
                        confirm_merge = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.BtnGroup-item.js-merge-commit-button').click()
                        time.sleep(3)
                        op_close_message = f'New closed pull request created - {is_pass}'
                    except:
                        op_close_message = f'sample-branch-1 has no commit. Unable to create pull request - {is_fail}'

                    #open pr
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/compare')
                    time.sleep(2)
                    pr_btn = driver.find_elements(By.CSS_SELECTOR,'.Button-label')
                    for elem in pr_btn:
                        if 'compare' in elem.text:
                            elem.click()
                            time.sleep(1)
                            branch_list = driver.find_elements(By.CLASS_NAME,'SelectMenu-item')
                            for branch in branch_list:
                                if branch.text == 'sample-branch-2':
                                    branch2_message = f'{branch.text} found - {is_pass}'
                                    branch.click()
                                    time.sleep(3)
                                    break
                            break
                    else:
                        branch2_message = f'sample-branch-2 not found - {is_fail}'
                    try:
                        #if branch 2 has commit
                        driver.find_element(By.CSS_SELECTOR,'.js-details-target.btn-primary.btn').click()
                        time.sleep(2)
                        driver.find_element(By.ID,'pull_request_title').send_keys('Close Pull Request')
                        create_pr = driver.find_element(By.CSS_SELECTOR, '.hx_create-pr-button.js-sync-select-menu-button.btn-primary.btn.BtnGroup-item.flex-auto').click()
                        time.sleep(2)
                        op_open_message = f'New open pull request created - {is_pass}'
                    except:
                        op_open_message = f'sample-branch-2 has no commit. Unable to create pull request - {is_fail}'

                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete}\n  {branch1_message}\n  {op_close_message}\n  {branch2_message}\n  {op_open_message}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)

                checkpoint(f'Verification {__class__.__name__}')
                pr_open_list = []
                pr_close_list = []
                #open pr
                try:
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/pulls?q=is%3Aopen+is%3Apr')
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative')
                    pr_open = driver.find_elements(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative .flex-auto.min-width-0.p-2.pr-3.pr-md-2 .Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
                    for elem in pr_open:
                        pr_open_list.append(elem.text)
                    message1 = f'{len(pr_open_list)} Open Pull Request - {is_pass}'
                except:
                    message1 = f'No Open Pull Request - {is_fail}'
                
                #close pr
                try:
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/pulls?q=is%3Apr+is%3Aclosed')
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative')
                    pr_close = driver.find_elements(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative .flex-auto.min-width-0.p-2.pr-3.pr-md-2 .Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
                    for elem in pr_close:
                        pr_close_list.append(elem.text)
                    message2 = f'{len(pr_close_list)} Closed Pull Request - {is_pass}'
                except:
                    message2 = f'No Closed Pull Request - {is_fail}'

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1} \n    {pr_open_list} \n  {message2} \n    {pr_close_list}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_incomplete}. {message}'
                operation_message = f'{__class__.__name__} Data - {is_incomplete}. \n  {message}'
                print(operation_message)

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.'
            print(operation_message)

        print(verify_message) 
        
        return version, operation_message, verify_message
    
class LFSData:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            checkpoint(f'Operation {__class__.__name__}')
            if verify_data == False:
                op_message = f'Operation LFSData cannot be automated - {is_skip}'
                operation = True
            else:
                operation = False

            if operation:
                operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
            else:
                operation_message = f'{__class__.__name__} Data - {is_skip}'
            print(operation_message)

            checkpoint(f'Verification {__class__.__name__}')
            driver.get(f'{url}/{name['OrganizationBasic']}/data/')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                verify_status = False
            except:
                verify_status = True

            if verify_status == True:
                file_list = driver.find_elements(By.CSS_SELECTOR,'.Box-row.Box-row--focus-gray.py-2.d-flex.position-relative.js-navigation-item')
                for file in file_list:
                    filename = file.find_element(By.CSS_SELECTOR, '.css-truncate.css-truncate-target.d-block.width-fit a')
                    if '.psd' in filename.text:
                        status = True
                        #render psd
                        filename.click()
                        time.sleep(5)
                        try:
                            render = driver.find_element(By.CSS_SELECTOR,'.render-shell.js-render-shell').text
                            if render == 'Unable to render rich display':
                                message = f'Unable to render psd file - {is_fail}'
                        except:
                            message = f'Able to render psd file - {is_pass}'
                        break
                else:
                    status = False
                    message = f'No LFS Data Found - {is_fail}'

                if status == True:
                    verify_message = f'Verification LFS Data - {is_complete} \n  {message}'
                elif status == False:
                    verify_message = f'Verification LFS Data - {is_complete}. \n  {message}'
            
            elif verify_status == False:
                verify_message = f'Verification LFS Data - {is_incomplete}. \n  No such url {url}/{name['OrganizationBasic']}/data/'
        
        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)

        print(verify_message)

        return version, operation_message, verify_message

class Release:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True

            if verify_status:
                checkpoint(f'Operation {__class__.__name__}')
                if verify_data == False:
                    wait = WebDriverWait(driver, 5)
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/releases/new')  
                    time.sleep(2)
                    release_tag = driver.find_element(By.CSS_SELECTOR, '.octicon.octicon-tag.mr-2').click()
                    time.sleep(3)
                    input_tag = driver.find_element(By.CSS_SELECTOR, '.SelectMenu-input.form-control').send_keys('Sample-Release-Tag')
                    time.sleep(2)
                    try:
                        #if tag exist
                        driver.find_element(By.CSS_SELECTOR,'.SelectMenu-list .SelectMenu-item .flex-1.css-truncate.css-truncate-overflow.is-filtering').click()
                    except:
                        choose_tag = driver.find_element(By.CSS_SELECTOR,'.SelectMenu-item.text-bold').click()
                    time.sleep(2)
                    release_name = driver.find_element(By.ID, 'release_name').send_keys('Sample Release Name')
                    time.sleep(2)   
                    release_desc = driver.find_element(By.ID, 'release_body').send_keys('Sample Release Description')
                    time.sleep(2)   
                    release_binary = driver.find_element(By.CSS_SELECTOR, '.sr-only.show-on-focus.color-bg-subtle.py-3.width-full.text-center')
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sr-only.show-on-focus.color-bg-subtle.py-3.width-full.text-center")))
                    release_binary.send_keys(os.getcwd()+"/assets/test.ghl")
                    time.sleep(6)   
                    release_submit = driver.find_element(By.CSS_SELECTOR,'.btn.btn-primary.js-publish-release').click()
                    time.sleep(3)
                    op_message = f'Sample Release Data Created - {is_pass}'
                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)
                
                 
                checkpoint(f'Verification {__class__.__name__}')
                driver.get(f'{url}/{name['OrganizationBasic']}/data/releases')
                time.sleep(2)
                try:
                    rel = driver.find_element(By.CSS_SELECTOR,'.d-inline.mr-3 a') 
                    message1 = f'\'{rel.text}\' Releases found - {is_pass}'
                except:
                    message1 = f'No Releases found - {is_fail}'

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_incomplete}. {message}'

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)

        print(verify_message)

        return version, operation_message, verify_message

class Package:
    def run(self, driver, url, version, verify_data):
        checkpoint(f'Operation {__class__.__name__}')
        if verify_data == False:
            #workflow
            crtpkg = True
            driver.get(f'{url}/{name['OrganizationBasic']}/data/new/main?filename=.github%2Fworkflows%2Fnpm-publish-github-packages.yml&workflow_template=ci%2Fnpm-publish-github-packages')
            time.sleep(3)

            if crtpkg:
                driver.find_element(By.CSS_SELECTOR,'.btn-primary.btn.float-right').click()
                time.sleep(1)
                driver.find_element(By.ID,'submit-file').click()
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-error')
                    op_message1 = f'github package worklow already existed - {is_pass}'
                except:
                    op_message1 = f'github package workflow created - {is_pass}'
            
            #package data
            op_message2 = f'Cannot automate Packages data. Please add manually - {is_skip}'

        operation_message  = f'{__class__.__name__} Data - {is_complete}\n  {op_message1}\n  {op_message2}'
        print(operation_message)

        checkpoint(f'Verification {__class__.__name__}')
        driver.get(f'{url}/{name['OrganizationBasic']}')
        time.sleep(2)
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            verify_status = False
        except:
            verify_status = True

        if verify_status == True:
            #workflow
            driver.get(f'{url}/{name['OrganizationBasic']}/data/tree/main/.github/workflows')
            file_list = driver.find_elements(By.CSS_SELECTOR,'.css-truncate.css-truncate-target.d-block.width-fit')
            for file in file_list: 
                if file.text == 'npm-publish-github-packages.yml':
                    message1 = f'Package workflow found! - {is_pass}'
                    break
            else:
                message1 = f'Package workflow not found - {is_fail}'

            driver.get(f'{url}/{name['OrganizationBasic']}/data/packages')
            pkg_list = []
            try:
                parent = driver.find_element(By.ID,'package-results')
                parent.find_element(By.CSS_SELECTOR,'.Box-row .d-flex .flex-auto .text-bold.f4.Link--primary')
                packages_element = parent.find_elements(By.CSS_SELECTOR, '.Box-row .d-flex .flex-auto .text-bold.f4.Link--primary')
                for package in packages_element:
                    pkg_list.append(package.text)
                status = True
            except:
                status = False

            if status == True:
                verify_message = f'{__class__.__name__} Data - {is_complete}\n  {message1}\n  Package Data found: {pkg_list} - {is_pass}'
            elif status == False:
                verify_message = f'{__class__.__name__} Data - {is_complete}\n  {message1}\n  Package Data not found: {pkg_list} - {is_fail}'
        
        elif verify_status == False:
            verify_message = f'{__class__.__name__} Data -  {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.'

        print(verify_message)

        return version, operation_message, verify_message

class Issue:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True

            if verify_status: 
                checkpoint(f'Operation {__class__.__name__}')
                if verify_data == False:
                    category = ['Open','Close']
                    for cat in category:
                        driver.get(f'{url}/{name['OrganizationBasic']}/data/issues/new')  
                        time.sleep(3)
                        issue_title = driver.find_element(By.ID,'issue_title').send_keys(f'Sample {cat} Issue')
                        issue_comment = driver.find_element(By.ID, 'issue_body').send_keys(f"Sample {cat} Issue Description")
                        issue_image = driver.find_element(By.ID, 'fc-issue_body').send_keys(os.getcwd()+'/assets/sample_image.png')
                        time.sleep(6)
                        driver.find_element(By.CSS_SELECTOR,'.flex-items-center.flex-justify-end.mx-2.mb-2.px-0.d-none.d-md-flex .btn-primary.btn').click()
                        time.sleep(3)
                        if cat == 'Open':
                            op_message1 = f'New {cat} issue data created - {is_pass}'
                        else:
                            driver.find_element(By.ID,'new_comment_field').send_keys('Closing issue')
                            driver.find_element(By.NAME,'comment_and_close').click()
                            time.sleep(1)
                            op_message2 = f'New {cat} issue data created - {is_pass}'
                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message1}\n  {op_message2}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)
                
                checkpoint(f'Verification {__class__.__name__}')    
                issue_open_list = []
                issue_close_list = []
                #open issue
                try:
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/issues?q=is%3Aopen+is%3Aissue')
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative')
                    issue_open = driver.find_elements(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative .flex-auto.min-width-0.p-2.pr-3.pr-md-2 .Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
                    for elem in issue_open:
                        issue_open_list.append(elem.text)
                    message1 = f'{len(issue_open_list)} Open Issue - {is_pass}'
                except:
                    message1 = f'No Open Issue - {is_fail}'
                
                #close issue
                #v3.7
                try:
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/issues?q=is%3Aissue+is%3Aclosed')
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative')
                    issue_close = driver.find_elements(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative .flex-auto.min-width-0.p-2.pr-3.pr-md-2 .Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
                    for elem in issue_close:
                        issue_close_list.append(elem.text)
                    message2 = f'{len(issue_close_list)} Closed Issue - {is_pass}'
                except:
                    message2 = f'No Closed Issue - {is_fail}'

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1} \n    {issue_open_list} \n  {message2} \n    {issue_close_list}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_fail}. {message}'

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)

        print(verify_message)

        return version, operation_message, verify_message

class Project:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True

            if verify_status:
                checkpoint(f'Operation {__class__.__name__}')
                if verify_data == False: 
                    category = ['Open','Close']
                    for cat in category:
                        driver.get(f'{url}/{name['OrganizationBasic']}/data/projects/new')  
                        time.sleep(3)
                        project_name = driver.find_element(By.ID, 'project_name').send_keys(f"Sample {cat} Project")
                        project_desc = driver.find_element(By.ID, 'project_body').send_keys(f"Sample {cat} project Description")
                        project_template_list = driver.find_element(By.CSS_SELECTOR, '.btn.select-menu-button.text-center.flex-auto').click()
                        time.sleep(2)
                        parent = driver.find_elements(By.CSS_SELECTOR,'.select-menu-list .select-menu-item .select-menu-item-text .select-menu-item-heading')
                        for elem in parent:
                            if elem.text == 'Basic kanban':
                                elem.click()
                                break
                        else:
                            pass
                        project_create = driver.find_element(By.CSS_SELECTOR, '.form-actions.d-flex.d-md-block.mb-4 .btn-primary.btn.float-none.float-md-left.flex-auto').click()
                        time.sleep(3)
                        if cat == 'Open':
                            op_message1 = f'New {cat} Project Data Basic Kanban Created - {is_pass}'
                        else:
                            time.sleep(3)
                            cname = '.project-pane.js-project-pane.js-project-triage-pane.js-build-status-to-the-left.border-left.border-bottom.position-relative.bottom-0.top-0.right-0.overflow-auto.ws-normal.hide-sm.height-full.width-full.project-touch-scrolling'
                            bname = '.pl-3.f5 .octicon.octicon-chevron-left'
                            driver.find_element(By.CSS_SELECTOR,f'{cname} {bname}').click()
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR,'.p-3.markdown-body.f5.border-bottom .js-project-dialog-button.btn-sm.btn.float-right').click()
                            time.sleep(2)
                            driver.find_element(By.CSS_SELECTOR,'.d-flex.d-sm-block .btn.flex-auto').click()
                            time.sleep(3)
                            op_message2 = f'New {cat} Project Data Basic Kanban Created - {is_pass}'
                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message1}\n  {op_message2}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)
                
                checkpoint(f'Verification {__class__.__name__}')
                project_open_list = []
                project_close_list = []
                #open project
                try:
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/projects?query=is%3Aopen&type=classic')
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.Box-row.clearfix.position-relative.pr-6')
                    pj_open = driver.find_elements(By.CSS_SELECTOR,'.Box-row.clearfix.position-relative.pr-6')
                    for elem in pj_open:
                        pname = elem.find_element(By.CSS_SELECTOR,'.col-12.col-md-6.col-lg-4.pr-2.float-left .mb-1 a')
                        project_open_list.append(pname.text)
                    message1 = f'{len(project_open_list)} Open Project - {is_pass}'
                except:
                    message1 = f'No Open Project - {is_fail}'
                project_open_list_f = []
                for item in project_open_list:
                    lines = item.splitlines()
                    project_open_list_f.extend(lines)

                #close project
                try:
                    driver.get(f'{url}/{name['OrganizationBasic']}/data/projects?query=is%3Aclosed&type=classic')
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.Box-row.clearfix.position-relative.pr-6')
                    pj_close = driver.find_elements(By.CSS_SELECTOR,'.Box-row.clearfix.position-relative.pr-6')
                    for elem in pj_close:
                        pname = elem.find_element(By.CSS_SELECTOR,'.col-12.col-md-6.col-lg-4.pr-2.float-left .mb-1 a')
                        project_close_list.append(pname.text)
                    message2 = f'{len(project_close_list)} Closed Project - {is_pass}'
                except:
                    message2 = f'No Closed Project - {is_fail}'
                project_close_list_f = []
                for item in project_close_list:
                    lines = item.splitlines()
                    project_close_list_f.extend(lines)

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1} \n    {project_open_list_f} \n  {message2} \n    {project_close_list_f}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_fail}. {message}'

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)

        print(verify_message)

        return version, operation_message, verify_message

class Wiki:
     def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True

            if verify_status:
                checkpoint(f'Operation {__class__.__name__}')
                if verify_data == False:
                    #v3.7
                    for page in range(1,3):
                        wiki_open_page = driver.get(f'{url}/{name['OrganizationBasic']}/data/wiki/_new')
                        time.sleep(1)
                        wiki_home_title = driver.find_element(By.ID,'gollum-editor-page-title')
                        wiki_home_title.clear()
                        wiki_home_title.send_keys(f'Wiki page{page}')
                        wiki_detail_clear = driver.find_element(By.ID, 'gollum-editor-body')
                        wiki_detail_clear.clear()
                        wiki_detail_clear.send_keys(f"Welcome to the testing wiki page{page}!")
                        wiki_attach_image = driver.find_element(By.ID, 'wiki-fileupload').send_keys(os.getcwd()+'/assets/sample_image.png')
                        time.sleep(6)
                        wiki_edit_message_field = driver.find_element(By.ID,'gollum-editor-message-field')
                        wiki_edit_message_field.clear()
                        wiki_edit_message_field.send_keys(f'test wiki page{page}')
                        time.sleep(3)
                        wiki_page_submit = driver.find_element(By.CSS_SELECTOR,'.flex-auto.btn.btn-primary').click()
                        time.sleep(3)
                    op_message = f'New wiki data created - {is_pass}'
                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)
                
                 
                checkpoint(f'Verification {__class__.__name__}')
                driver.get(f'{url}/{name['OrganizationBasic']}/data/wiki')
                time.sleep(2)
                try:
                    wik = driver.find_element(By.ID,'wiki-pages-box').click()
                    wiki = True
                except:
                    wiki = False

                if wiki:
                    wiki_list = []
                    wik_box = driver.find_elements(By.CSS_SELECTOR,'.Box-row.px-2.py-2')
                    for elem in wik_box:
                        pg = elem.find_element(By.CSS_SELECTOR,'.d-flex.flex-items-start').text
                        wiki_list.append(pg)
                    message1 = f' Wiki Page found - {wiki_list}'
                else:
                    message1 = f'No Wiki found - {is_fail}'

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1}'
            else:
                verify_message = f'{__class__.__name__} Data - {is_fail}. {message}'

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)

        print(verify_message)

        return version, operation_message, verify_message
        
class Webhook:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            driver.get(f'{url}/{name['OrganizationBasic']}/data')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'data\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True

            if verify_status:
                checkpoint(f'Operation {__class__.__name__}')
                if verify_data == False:
                    try:
                        driver.get(f'{url}/{name['OrganizationBasic']}/data/settings/hooks')
                        time.sleep(2)
                        driver.find_element(By.CSS_SELECTOR,'.listgroup-item.hook-item.clearfix.success.d-flex.flex-md-row.flex-column')
                        op_message = f'Webhook Already Existed - {is_pass}'
                    except:
                        config = load_config()
                        payload = config.get('webhook_setting','payload_url')
                        driver.get(f'{url}/{name['OrganizationBasic']}/data/settings/hooks/new')  
                        hook_url = driver.find_element(By.ID, 'hook_url').send_keys(payload)
                        time.sleep(3)
                        hook_content = Select(driver.find_element(By.ID, 'hook_content_type')).select_by_value('json')
                        time.sleep(3)
                        hook_opt = driver.find_element(By.ID, 'hook-event-choice-everything').click()
                        time.sleep(3)
                        hook_create = driver.find_element(By.CSS_SELECTOR, 'p .btn-primary.btn').click()
                        driver.implicitly_wait(5)
                        time.sleep(3)
                        op_message = f'New webhook data created - {is_pass}'
                    operation = True
                else:
                    operation = False

                if operation:
                    operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
                else:
                    operation_message = f'{__class__.__name__} Data - {is_skip}'
                print(operation_message)
                
                checkpoint(f'Verification {__class__.__name__}')
                driver.get(f'{url}/{name['OrganizationBasic']}/data/settings/hooks')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.listgroup-item.hook-item.clearfix.success.d-flex.flex-md-row.flex-column')
                    wh = True
                except:
                    wh = False

                if wh:
                    hook = driver.find_element(By.CSS_SELECTOR,'.mb-md-0.mb-2.flex-auto .css-truncate')
                    message1 = f'Webhook found: {hook.text} - {is_pass}'
                else:
                    message1 = f'No Webhook found - {is_fail}'

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1}'
            else:
                verify_message = f'{__class__.__name__} Data - {is_fail}. {message}'

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            print(operation_message)

        print(verify_message)

        return version, operation_message, verify_message
    
class PreReceiveHook:
    def run(self, driver, url, version, verify_data):
        checkpoint(f'Operation {__class__.__name__}')
        driver.get(f'{url}/{name['OrganizationBasic']}')
        time.sleep(3)
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            message = f'You are in the wrong path. Please ensure you are in {url}/{name['OrganizationBasic']} - {is_fail}'
            op = False 
        except:
            op = True
        
        if op:
            if verify_data == False:
                #NOTE upload file
                driver.get(f'{url}/{name['OrganizationBasic']}/data/upload/main')
                time.sleep(3)
                driver.find_element(By.ID,'upload-manifest-files-input').send_keys(os.getcwd()+'/assets/pre_receive_hooks_spec.rb')
                time.sleep(6)
                driver.find_element(By.CSS_SELECTOR,'.js-blob-submit.btn-primary.btn').click()
                time.sleep(3)
                #NOTE create prh
                driver.get(f'{url}/enterprises/github/settings/hooks')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.listgroup') 
                    op_message = f'Pre-Receive Hook already existed - {is_pass}'
                except:
                    driver.get(f'{url}/enterprises/github/settings/pre_receive_hook_targets/new')
                    driver.find_element(By.ID,'pre_receive_hook_target_hook_attributes_name').send_keys("Sample Pre-Receive Hook")
                    driver.find_element(By.CSS_SELECTOR, '.select-menu.select-menu-inline.details-reset.details-overlay').click()
                    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search repositories"]').send_keys(f'{name['OrganizationBasic']}/data')
                    time.sleep(2)
                    driver.find_element(By.ID,'repo-menu').click()
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.script-group').click()
                    time.sleep(2)
                    parent = driver.find_elements(By.CSS_SELECTOR,'.script-group .js-file-results .select-menu-list .select-menu-item.width-full .select-menu-item-text')
                    for elem in parent:
                        if elem.text == 'pre_receive_hooks_spec.rb':
                            elem.click()
                            break
                    else:
                        pass
                    driver.find_element(By.ID,'pre_receive_hook_target_hook_attributes_enable').click()
                    driver.find_element(By.CSS_SELECTOR,'.form-action-spacious.btn-primary.btn').click()
                    time.sleep(3)
                    op_message = f'New prereceive data created - {is_pass}'
                operation = True
            else:
                operation = False

            if operation:
                operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
            else:
                operation_message = f'{__class__.__name__} Data - {is_skip}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
        print(operation_message)

        checkpoint(f'Verification {__class__.__name__}')
        driver.get(f'{url}/{name['OrganizationBasic']}/data')
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            message = f'You are in the wrong path. Please ensure you are in {url}/{name['OrganizationBasic']}/data - {is_fail}'
            file_url_status = False 
            file_status = False
        except:
            file_url_status = True 

        #NOTE if correct repo
        if file_url_status == True:
            file_list = driver.find_elements(By.CSS_SELECTOR,'.Box-row.Box-row--focus-gray.py-2.d-flex.position-relative.js-navigation-item')
            for file in file_list:
                filename = file.find_element(By.CSS_SELECTOR, '.css-truncate.css-truncate-target.d-block.width-fit a')
                if filename.text == 'pre_receive_hooks_spec.rb':
                    file_status = True
                    break
                else:
                    file_status = False #no file found
            else:
                pass
        
        #NOTE if pre_receive_hooks_spec.rb found
        if file_status == True:
            driver.get(f'{url}/{name['OrganizationBasic']}/data/settings/hooks')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                hook_url_status = False
            except:
                hook_url_status = True 

            #NOTE if correct hook url
            if hook_url_status == True: 
                driver.get(f'{url}/enterprises/github/settings/hooks')
                try:
                    driver.find_element(By.CSS_SELECTOR,'.listgroup-item.pre-receive-hook-list.disabled') 
                    prh_status = True
                except:
                    prh_status = False

                #NOTE if hook data found, get all 
                if prh_status == True:
                    prh_list = driver.find_elements(By.CSS_SELECTOR,'.listgroup .content strong')
                    for prh in prh_list:
                        message = f'Pre-receive hook data - {prh.text}'
                    verify_status = True
                elif prh_status == False:
                    message = f'Pre-receive hook data not found - {is_fail}'
                    verify_status = False

                if verify_status:
                    #enable hook enforcement
                    driver.get(f'{url}/enterprises/github/settings/pre_receive_hook_targets/1')
                    time.sleep(2)
                    driver.find_element(By.ID,'pre_receive_hook_target_hook_attributes_enable').click() #2nd checckbox
                    driver.find_element(By.CSS_SELECTOR,'.form-action-spacious.btn-primary.btn').click() #save button
                    time.sleep(3)
                    #commit test file
                    driver.get(f'{url}/{name['OrganizationBasic']}/data')
                    time.sleep(3)
                    driver.find_element(By.CSS_SELECTOR, '.d-none.d-md-flex.flex-items-center').click()
                    driver.find_element(By.CSS_SELECTOR, '.dropdown-item.btn-link').click()
                    driver.find_element(By.NAME, 'filename').send_keys('prh.txt')
                    driver.find_element(By.CLASS_NAME, 'CodeMirror-line').send_keys("test pre receive hook commit")
                    driver.find_element(By.ID, 'submit-file').click()
                    time.sleep(3)
                    #verify hook enforcement
                    try:
                        prhmsg = driver.find_element(By.CSS_SELECTOR,'.prereceive-feedback-heading')
                        message2 = f'Pre Receive Hook Enforcement - {is_pass}'
                    except:
                        message2 = f'Pre Receive Hook Enforcement - {is_fail}'
                    #disable hook enforcement
                    driver.get(f'{url}/enterprises/github/settings/pre_receive_hook_targets/1')
                    time.sleep(2)
                    driver.find_element(By.ID,'pre_receive_hook_target_hook_attributes_enable').click() #2nd checckbox
                    driver.find_element(By.CSS_SELECTOR,'.form-action-spacious.btn-primary.btn').click() #save button
                    time.sleep(3)
                
                #NOTE prh verification message
                if verify_status == True:
                    verify_message = f'{__class__.__name__} Data - {is_complete}\n  {message}\n  {message2}'
                elif verify_status == False:
                    verify_message = f'{__class__.__name__} Data - {is_complete}\n  {message}'
            elif hook_url_status == False:
                verify_message = f'{__class__.__name__} Data - {is_incomplete}. Wrong Hook Url'

        elif file_status == False:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.'

        print(verify_message)

        return version, operation_message, verify_message
    
class OrganizationSecurityAlerts:
    def run(self, driver, url, version, verify_data):
        checkpoint(f'Operation {__class__.__name__}')
        if verify_data == False:
            driver.get(f'{url}/organizations/new')
            driver.find_element(By.CSS_SELECTOR, '.form-control.js-new-organization-name.width-full.py-1').send_keys(alert_org)
            time.sleep(2)
            try:
                driver.find_element(By.CSS_SELECTOR,'.form-control.js-new-organization-name.width-full.py-1.is-autocheck-errored')
                op_message = f'organization \'{name['OrganizationAlert']}\' already existed - {is_pass}'
            except:
                driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
                op_message = f'New organization \'{name['OrganizationAlert']}\' created - {is_pass}'
            name['OrganizationAlert'] = alert_org
            with open('naming.json', 'w') as file:
                json.dump(name, file, indent=4)
            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}'
        print(operation_message)
        
        checkpoint(f'Verification {__class__.__name__}')
        driver.get(f'{url}/{name['OrganizationAlert']}')
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            verify_status = False
        except:
            verify_status = True

        if verify_status == True:
            verify_message = f'{__class__.__name__} Data - {is_complete}. \n  Org \'{name['OrganizationAlert']}\' found - {is_pass}'
        elif verify_status == False:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. \n  Org \'{name['OrganizationAlert']}\' not found - {is_fail}'

        print(verify_message)

        return version, operation_message, verify_message

class RepoCodeScanning:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status == True:
            checkpoint(f'Operation {__class__.__name__}')
            if verify_data == False:
                #create repo code-scanning 
                driver.get(f'{url}/organizations/{name['OrganizationBasic']}/repositories/new')
                driver.get(f'{url}/organizations/{name['OrganizationBasic']}/repositories/new')
                driver.find_element(By.ID,'repository_name').send_keys('code-scanning')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.form-control.js-repo-name.js-repo-name-auto-check.short.is-autocheck-errored')
                    op_message1 = f'repo \'code-scanning\' already existed - {is_pass}'
                    driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning')
                except:
                    driver.find_element(By.ID,'repository_auto_init').click()
                    driver.find_element(By.CSS_SELECTOR,'.js-with-permission-fields .btn-primary.btn').click()
                    time.sleep(4)
                    op_message1 = f'Created repo \'code-scanning\' - {is_pass}'

                #add sample.js
                driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning')
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, '.d-none.d-md-flex.flex-items-center').click()
                driver.find_element(By.CSS_SELECTOR, '.dropdown-item.btn-link').click()
                driver.find_element(By.NAME, 'filename').send_keys('sample.js')
                driver.find_element(By.CLASS_NAME, 'CodeMirror-line').send_keys("const a = 1;")
                driver.find_element(By.ID, 'submit-file').click()
                time.sleep(3)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-error')
                    op_message2 = f'File \'sample.js\' already existed - {is_pass}'
                except:
                    op_message2 = f'Created file \'sample.js\' - {is_pass}'

                #advance setting
                driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning/settings/security_analysis')
                time.sleep(3) 
                parent_advsec = driver.find_element(By.CSS_SELECTOR, '.d-flex.flex-md-row.flex-column.flex-md-items-center.pt-3.mb-3.border-bottom.color-border-muted')
                desc_advsec = parent_advsec.find_element(By.CSS_SELECTOR, 'div.mb-md-0.mb-2.flex-auto h2')
                if desc_advsec.text == 'GitHub Advanced Security':
                    btn_advsec = parent_advsec.find_element(By.CSS_SELECTOR, '.BtnGroup.flex-auto')
                    if btn_advsec.text == 'Enable':
                        btn_advsec.click()
                        time.sleep(3)
                        parent_advsec.find_element(By.CSS_SELECTOR, '.btn.btn-block.ws-normal').click()
                        time.sleep(2)
                    else:
                        pass
                op_message3 = f'Advance Setting Enabled - {is_pass}'

                #workflow
                driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning/actions/new')
                try:
                    driver.find_element(By.CLASS_NAME, 'font-mktg')
                    op_message4 = f'Instance is in cluster mode - {is_skip}'
                except:
                    wflow = driver.find_elements(By.CSS_SELECTOR,'.Box.rounded-2.d-flex.flex-column.overflow-hidden.width-full.flex-auto.mb-3')
                    for elem in wflow:
                        try:
                            elemtxt = elem.find_element(By.CSS_SELECTOR,'.d-flex.flex-justify-between.px-4.pt-3.pb-0 .pr-4 h5')
                            if elemtxt.text == 'CodeQL Analysis':
                                elem.find_element(By.CSS_SELECTOR,'.d-flex.flex-column.flex-auto.flex-justify-between .d-flex.flex-justify-between.flex-items-center.pt-2.pb-4.px-4 .btn.btn-sm').click()
                                break
                        except:
                            continue
                    else:
                        pass
                    time.sleep(4)
                    driver.find_element(By.CSS_SELECTOR,'.btn-primary.btn.float-right').click()
                    time.sleep(1)
                    driver.find_element(By.ID,'submit-file').click()
                    time.sleep(2)
                    try:
                        driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-error')
                        op_message4 = f'worklow already existed - {is_pass}'
                    except:
                        op_message4 = f'workflow created - {is_pass}'

                # Wrong js file
                driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning/upload/main')
                time.sleep(3)
                driver.find_element(By.ID,'upload-manifest-files-input').send_keys(os.getcwd()+'/assets/wrong.js')
                time.sleep(6)
                driver.find_element(By.CSS_SELECTOR,'.js-blob-submit.btn-primary.btn').click()
                time.sleep(3)
                op_message5 = f'Uploaded wrong.js file - {is_pass}'

                op_message6 = f'Please create runner manually - {is_skip}'
                operation = True
            else:
                operation = False

            if operation:
                operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message1} \n  {op_message2} \n  {op_message3}\n  {op_message4} \n  {op_message5}\n  {op_message6}'
            else:
                operation_message = f'{__class__.__name__} Data - {is_skip}'
            print(operation_message)
            
            checkpoint(f'Verification {__class__.__name__}')
            driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'code-scanning\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True
            
            if verify_status == True:
                #v3.7
                file_list = driver.find_elements(By.CSS_SELECTOR,'.css-truncate.css-truncate-target.d-block.width-fit')
                #sample js file
                for file in file_list:
                    if file.text == 'sample.js':
                        message1 = f'file sample.js found! - {is_pass}'
                        break
                    else:
                        continue
                else:
                    message1 = f'file sample.js not found - {is_fail}'

                # wrong js file
                for file in file_list:
                    if file.text == 'wrong.js':
                        message1_2 = f'file wrong.js found! - {is_pass}'
                        break
                    else:
                        continue
                else:
                    message1_2 = f'file wrong.js not found - {is_fail}'
                
                #workflow
                driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning/tree/main/.github/workflows')
                file_list = driver.find_elements(By.CSS_SELECTOR,'.css-truncate.css-truncate-target.d-block.width-fit')
                workflowname = 'codeql.yml'
                for file in file_list: 
                    if file.text == workflowname:
                        message2 = f'workflow found! - {is_pass}'
                        break
                else:
                    message2 = f'workflow not found - {is_fail}'
                
                #runner
                driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning/settings/actions/runners')
                try:
                    runner = driver.find_element(By.CSS_SELECTOR,'.h4.color-fg-default')
                    message3 = f'runner round on this repo = {runner.text} - {is_pass}'
                except:
                    message3 = f'no runner found on this repo. Please add runner manually - {is_fail}'
   
            if verify_status == True:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1}\n  {message1_2} \n  {message2} \n  {message3}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_complete}. {message}'

        elif org_status == False:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.'
            print(operation_message)

        print(verify_message)

        return version, operation_message, verify_message

class RepoDependabot:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status == True:
            checkpoint('STARTING REPO DEPENDABOT OPERATION')
            if verify_data == False:
                #create repo dependabot 
                driver.get(f'{url}/organizations/{name['OrganizationBasic']}/repositories/new')
                driver.get(f'{url}/organizations/{name['OrganizationBasic']}/repositories/new')
                driver.find_element(By.ID,'repository_name').send_keys('dependabot')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.form-control.js-repo-name.js-repo-name-auto-check.short.is-autocheck-errored')
                    op_message1 = f'repo \'dependabot\' already existed - {is_pass}'
                except:
                    driver.find_element(By.ID,'repository_auto_init').click()
                    driver.find_element(By.CSS_SELECTOR,'.js-with-permission-fields .btn-primary.btn').click()
                    op_message1 = f'repo \'dependabot\' created'
                    time.sleep(3)

                #add dependabot alert files
                op_message2 = f'Sorry, dependabot files cannot be automated. Please add them manually.'

                #enable dependabot
                #v3.11
                driver.get(f'{url}/{name['OrganizationBasic']}/dependabot/settings/security_analysis')
                parentdep = driver.find_elements(By.CSS_SELECTOR,'.ml-4.py-3')
                for elem in parentdep:
                    dep = elem.find_element(By.CSS_SELECTOR,'.mr-md-4.mb-md-0.mb-2.flex-auto h4')
                    if dep.text == 'Dependabot alerts':
                        try:
                            depnew = elem.find_element(By.CSS_SELECTOR,'.BtnGroup.flex-auto')
                            if depnew.text == 'Disable':
                                op_message3 = f'Dependabot has been enabled - {is_pass}'
                            else:
                                depnew.click()
                                op_message3 = f'Dependabot enabled - {is_pass}'
                            break
                        except:
                                op_message3 = f'Github connect not connected - {is_fail}'
                else:
                    op_message3 = f'Unable to find dependabot alerts button - {is_fail}'

                op_message4 = f'Please create runner manually - {is_skip}'
                operation = True
            else:
                operation = False

            if operation:
                operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message1}\n  {op_message2}\n  {op_message3}\n  {op_message4}'
            else:
                operation_message = f'{__class__.__name__} Data - {is_skip}'
            print(operation_message)

            checkpoint(f'Verification {__class__.__name__}')
            driver.get(f'{url}/{name['OrganizationBasic']}/dependabot')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'dependabot\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True

            if verify_status == True:
                #depenabot files:
                #v3.7
                driver.get(f'{url}/{name['OrganizationBasic']}/dependabot')
                files = ['.github','sample-packages','.gitignore','LICENSE','index.js','package-lock.json','package.json']
                message1_list = []
                file_list = driver.find_elements(By.CSS_SELECTOR,'.flex-auto.min-width-0.col-md-2.mr-3 .css-truncate.css-truncate-target.d-block.width-fit')
                for file in file_list:
                    if file.text in files:
                        message1 = f'{file.text}'
                    else:
                        message1 = f'{file.text}'
                    message1_list.append(message1)
                for item1 in message1_list:
                    for item2 in files:
                        if item1 == item2:
                            message = f'Dependabot files found - {is_pass}'
                        else:
                            message = f'Dependabot files not found - {is_fail}'

                #dependabot enabled
                driver.get(f'{url}/{name['OrganizationBasic']}/dependabot/security')
                dep_setting = driver.find_elements(By.CSS_SELECTOR,'.flex-auto.mr-2')
                for elem in dep_setting:
                    dep_text = elem.find_element(By.CLASS_NAME,'text-bold')
                    if dep_text.text == 'Dependabot alerts •':
                        try:
                            dep_status = elem.find_element(By.CSS_SELECTOR,'.text-bold.color-fg-success')
                            message2 = f'Dependabot is enabled - {is_pass}'
                            break
                        except:
                            message2 = f'dependabot is not enabled - {is_fail}'
                            break
                    else:
                        continue
                else:
                    message2 = f'dependabot setting not found - {is_fail}'

                #dependabot alerts
                driver.get(f'{url}/{name['OrganizationBasic']}/dependabot/security/dependabot')
                #v3.11
                try:
                    driver.find_element(By.CSS_SELECTOR,'.blankslate.blankslate-large.blankslate-spacious')
                    githubconnect = False
                except:
                    githubconnect = True
                
                if githubconnect:
                    displaymessage = driver.find_element(By.CSS_SELECTOR,'.blankslate-heading')
                    if displaymessage.text == 'Welcome to Dependabot alerts!':
                        depalert = False
                    else:
                        depalert = True
                else:
                    depalert = False

                message3_list = []
                if depalert == True:
                    dep_alerts = driver.find_elements(By.CSS_SELECTOR,'.Link--primary.no-underline.f4.text-bold.v-align-middle')
                    message3 = f'{len(dep_alerts)} dependabot alerts found: - {is_pass}'
                    for alert in dep_alerts:
                        message3_list.append(alert.text)
                elif depalert == False:
                    message3 = f'Dependabot has no alerts - {is_fail}'
        
            if verify_status == True:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message} \n    {message1_list} \n  {message2} \n  {message3} \n    {message3_list}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_complete}. {message}'
        
        elif org_status == False:
            verify_message = f'Verification {__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'Operation {__class__.__name__} Data - {is_incomplete}. Org \'runner\' not found. Please create first.'
            print(operation_message)

        print(verify_message)
        
        return version, operation_message, verify_message

class RepoSecretScanning: 
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/{name['OrganizationBasic']}')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            org_status = False
        except:
            org_status = True

        if org_status:
            checkpoint(f'STARTING {__class__.__name__} OPERATION')
            if verify_data == False:
                #create repo dependabot 
                driver.get(f'{url}/organizations/{name['OrganizationBasic']}/repositories/new')
                driver.get(f'{url}/organizations/{name['OrganizationBasic']}/repositories/new')
                driver.find_element(By.ID,'repository_name').send_keys('secret-scanning')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.form-control.js-repo-name.js-repo-name-auto-check.short.is-autocheck-errored')
                    op_message1 = f'repo \'secret-scanning\' already existed - {is_pass}'
                except:
                    driver.find_element(By.ID,'repository_auto_init').click()
                    driver.find_element(By.CSS_SELECTOR,'.js-with-permission-fields .btn-primary.btn').click()
                    op_message1 = f'repo \'secret-scanning\' created'
                    time.sleep(3)

                #advance setting Button
                driver.get(f'{url}/{name['OrganizationBasic']}/secret-scanning/settings/security_analysis') 
                time.sleep(3) 
                parent_advsec = driver.find_element(By.CSS_SELECTOR, '.d-flex.flex-md-row.flex-column.flex-md-items-center.pt-3.mb-3.border-bottom.color-border-muted')
                desc_advsec = parent_advsec.find_element(By.CSS_SELECTOR, '.mb-md-0.mb-2.flex-auto h2')
                if desc_advsec.text == 'GitHub Advanced Security':
                    btn_advsec = parent_advsec.find_element(By.CSS_SELECTOR, '.BtnGroup.flex-auto')
                    if btn_advsec.text == 'Enable':
                        btn_advsec.click()
                        time.sleep(3)
                        parent_advsec.find_element(By.CSS_SELECTOR, '.btn.btn-block.ws-normal').click()
                        time.sleep(2)
                    else:
                        pass
                op_message2 = f'Advance Setting Enabled - {is_pass}'

                #Secret Scanning 
                parent_ss = driver.find_elements(By.CSS_SELECTOR,'.d-flex.flex-md-row.flex-column.flex-md-items-center.pb-0.pt-2.color-border-muted')
                for elem in parent_ss:
                    desc_ss = elem.find_element(By.CSS_SELECTOR, '.mb-md-0.mb-2.flex-auto h3')
                    if desc_ss.text == 'Secret scanning':
                        btn_ss = elem.find_element(By.CSS_SELECTOR,'.BtnGroup.flex-auto')
                        if btn_ss.text == 'Enable':
                            btn_ss.click()
                            time.sleep(3)
                    else:
                        pass
                op_message5 = f'Secret Scanning Enabled - {is_pass}'

                #pattern
                driver.get(f'{url}/{name['OrganizationBasic']}/secret-scanning/settings/security_analysis/custom_patterns/new')
                time.sleep(3)
                try:
                    driver.find_element(By.CLASS_NAME, 'font-mktg')
                    create_pattern = False
                except:
                    create_pattern = True
                
                if create_pattern:
                    pattern_name = driver.find_element(By.ID, 'display_name').send_keys('My octocat pattern')
                    secret_format = driver.find_element(By.NAME,'secret_format').send_keys('octocat_token_[a-zA-Z0-9]{15}')
                    test_string = driver.find_element(By.CLASS_NAME, 'CodeMirror-code').send_keys('octocat_token_123456789qwerty')
                    time.sleep(2)
                    dry_run = driver.find_element(By.CSS_SELECTOR, '.d-flex.flex-items-center.mt-1 .js-custom-pattern-submit-button.btn-primary.btn').click()
                    for trial in range(4):
                        time.sleep(3)
                        try: #js-custom-pattern-submit-button btn-primary btn
                            driver.find_element(By.CSS_SELECTOR,'.js-custom-pattern-submit-button.btn-primary.btn').click()
                            break
                        except:
                            driver.refresh()
                    op_message3 = f'New Secret Pattern Published - {is_pass}'
                else:
                    op_message3 = f'Secret Scanning not enabled - {is_fail}'

                #add secret.txt
                driver.get(f'{url}/{name['OrganizationBasic']}/secret-scanning')
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, '.d-none.d-md-flex.flex-items-center').click()
                driver.find_element(By.CSS_SELECTOR, '.dropdown-item.btn-link').click()
                driver.find_element(By.NAME, 'filename').send_keys('secret.txt')
                driver.find_element(By.CLASS_NAME, 'CodeMirror-line').send_keys("awdawdawd\noctocat_token_123456789qwerty\nawdadwawd")
                driver.find_element(By.ID, 'submit-file').click()
                time.sleep(3)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-error')
                    op_message4 = f'File \'secret.txt\' already existed - {is_pass}'
                    driver.get(f'{url}/{name['OrganizationBasic']}/code-scanning')
                except:
                    op_message4 = f'Created file \'secret.txt\' - {is_pass}'
                operation = True
            else:
                operation = False
            
            if operation:
                operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message1}\n  {op_message2}\n  {op_message5}\n  {op_message3}\n  {op_message4}'
            else:
                operation_message = f'{__class__.__name__} Data - {is_skip}'
            print(operation_message)

            checkpoint(f'Verification {__class__.__name__}')
            driver.get(f'{url}/{name['OrganizationBasic']}/secret-scanning')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                message = f'Repo \'secret-scanning\' not found. Please check and add manually'
                verify_status = False
            except:
                verify_status = True
            
            if verify_status:
                #secret.txt file
                file_list = driver.find_elements(By.CSS_SELECTOR,'.css-truncate.css-truncate-target.d-block.width-fit')
                for file in file_list:
                    if file.text == 'secret.txt':
                        message1 = f'file secret.txt found! - {is_pass}'
                        break
                    else:
                        continue
                else:
                    message1 = f'file secret.txt not found - {is_fail}'

                #pattern
                driver.get(f'{url}/{name['OrganizationBasic']}/secret-scanning/settings/security_analysis')
                published_pattern_list = []
                try:
                    pattern_parent = driver.find_element(By.CSS_SELECTOR,'.Box.mb-4')
                    patterns = pattern_parent.find_elements(By.CSS_SELECTOR,'.Box-row')
                    for element in patterns:
                        pattern = element.find_element(By.CSS_SELECTOR,'.d-flex a')
                        try: #Label Label--secondary Label--large ml-2
                            element.find_element(By.CSS_SELECTOR,'.Label.Label--secondary.Label--large.ml-2')
                            continue
                        except:
                            published_pattern_list.append(pattern.text)
                    message2 = f'Published Pattern found - {is_pass}'
                except:
                    message2 = f'Published Pattern not found - {is_fail}'

                # SECRET ALERTS
                time.sleep(5)
                driver.get(f'{url}/{name['OrganizationBasic']}/secret-scanning/security/secret-scanning')
                time.sleep(2)
                try:
                    sectext = driver.find_element(By.CLASS_NAME,'mb-1').text
                    secalert = False
                except:
                    secalert = True

                message3_list = []
                if secalert: 
                    secret_alerts = driver.find_elements(By.CSS_SELECTOR,'.markdown-body.mr-1 .Truncate .Truncate-text')
                    message3 = f'{len(secret_alerts)} secret alerts found: - {is_pass}'
                    for alert in secret_alerts:
                        message3_list.append(alert.text)
                else:
                    message3 = f'Secret Scanning has no alerts - {is_fail}'
                    
            if verify_status == True:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message1} \n  {message2} \n    {published_pattern_list}\n  {message3}\n    {message3_list}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_complete}. {message}'

        elif org_status == False:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'{name['OrganizationBasic']}\' not found. Please create first.'
            print(operation_message)
        
        print(verify_message)

        return version, operation_message, verify_message
    
class OrganizationRunners:
    """
    This testcase is to create organization named runners, which will consist of runner from repo level, org leve, and ent level.
    """
    def run(self, driver, url, version, verify_data):
        checkpoint('STARTING RUNNERS OPERATION')
        if verify_data == False:
            driver.get(f'{url}/organizations/new')
            driver.find_element(By.CSS_SELECTOR, '.form-control.js-new-organization-name.width-full.py-1').send_keys('runners')
            time.sleep(3)
            try:
                driver.find_element(By.CSS_SELECTOR,'.form-control.js-new-organization-name.width-full.py-1.is-autocheck-errored')
                print('org runners already exist')
                op_message = f'organization \'runners\' already existed - {is_pass}'
            except:
                driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
                print('Organization runners created. please create runner manually')
                op_message = f'Org \'runners\' created. Please create runner manually.'
            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}'
        checkpoint('OPERATION RUNNERS COMPLETED')
        
        checkpoint("VERIFYING ORGANIZATIONRUNNER DATA")
        driver.get(f'{url}/runners')
        print('')
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            print(f'Organization runners not found')
            verify_status = False
        except:
            verify_status = True

        if verify_status == True:
            verify_message = f'{__class__.__name__} Data - {is_pass}'
        elif verify_status == False:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. \n  Org \'runners\' not found. - {is_fail}'

        checkpoint("ORGANIZATION DATA VERIFICATION COMPLETED")
        return version, operation_message, verify_message
    
class RepoRunner:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/runners')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            print(f'Organization runner not found')
            org_status = False
        except:
            org_status = True

        if org_status:
            checkpoint('STARTING REPO RUNNER OPERATION')
            if verify_data == False:
                operation = True
                driver.get(f'{url}/organizations/runners/repositories/new')
                driver.find_element(By.ID,'repository_name').send_keys('repo-runner')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.form-control.js-repo-name.js-repo-name-auto-check.short.is-autocheck-errored')
                    print('repo repo-runner already exist')
                    op_message = f'repo \'repo-runner\' already existed - {is_pass}'
                except:
                    driver.find_element(By.ID,'repository_auto_init').click()
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.js-with-permission-fields .btn-primary.btn').click()
                    print('Repo repo-runner created.')
                    time.sleep(3)
                    print('Sorry, self-hosted repo level runner cannot be automated. Please add manually')
                    op_message = f'Repo \'repo-runner\' created. Please create runner manually - {is_pass}'
            else:
                operation = False

            if operation:
                operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
            else:
                operation_message = f'{__class__.__name__} Data - {is_skip}'
            checkpoint('OPERATION REPO RUNNER COMPLETED')

            checkpoint("VERIFYING REPO-RUNNER DATA")
            driver.get(f'{url}/runners/repo-runner')
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, 'font-mktg')
                print(f'Repo repo-runner not found')
                message = f'Repo \'repo-runner\' not found. Please check and add manually - {is_fail}'
                verify_status = False
            except:
                verify_status = True

            if verify_status:
                #runner
                driver.get(f'{url}/runners/repo-runner/settings/actions/runners')
                message = f'Repo \'repo-runner\' found - {is_pass}'
                #v3.7
                try:
                    runner = driver.find_element(By.CSS_SELECTOR,'.h4.color-fg-default')
                    message1 = f'runner round on this repo = {runner.text} - {is_pass}'
                    print(f'Runner {runner.text} found!')
                except:
                    message1 = f'no runner found on this repo. Please add runner manually - {is_fail}'
                    print('No runner found.')

            if verify_status == True:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message} \n  {message1}'
            elif verify_status == False:
                verify_message = f'{__class__.__name__} Data - {is_complete} \n  {message}'
            checkpoint("REPO-RUNNER DATA VERIFICATION COMPLETED")
            
        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'runners\' not found. Please create first.' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete}. Org \'runners\' not found. Please create first.'
        return version, operation_message, verify_message
    
class OrgRunner:
    def run(self, driver, url, version, verify_data):
        try:
            driver.get(f'{url}/runners')
            time.sleep(3)
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            print(f'Organization runner not found')
            org_status = False
        except:
            org_status = True

        if org_status:
            checkpoint('STARTING ORGANIZATION RUNNER OPERATION')
            if verify_data == False:
                print('Sorry, self-hosted repo level runner cannot be automated. Please add manually')
            op_message = f'Sorry, self-hosted org level runner cannot be automated. Please add manually'
            operation_message = f'{__class__.__name__} Data - {is_skip} \n  {op_message}'
            checkpoint('OPERATION ORGANIZATION RUNNER COMPLETED')

            checkpoint("VERIFYING REPO-RUNNER DATA")
            #org runner
            driver.get(f'{url}/organizations/runners/settings/actions/runners')
            #v3.7
            try:
                runner = driver.find_element(By.CSS_SELECTOR,'.h4.color-fg-default')
                message = f'runner round on this organization = {runner.text} - {is_pass}'
                print(f'Runner {runner.text} found!')
                verify_status = True
            except:
                message = f'no runner found on this organization. Please add runner manually - {is_fail}'
                print('No runner found.')
                verify_status = False

            if verify_status:
                v_message = f'{__class__.__name__} Data - {is_complete}'
                verify_message = f'{v_message} \n  {message}'
            else:
                verify_message = f'{__class__.__name__} Data - {is_complete} \n  {message}'
            checkpoint("REPO-RUNNER DATA VERIFICATION COMPLETED")

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. \n  Org \'runners\' not found. Please create first - {is_fail}' 
            operation_message = f'{__class__.__name__} Data - {is_incomplete} \n  Org \'runners\' not found. Please create first - {is_fail}'
        
        return version, operation_message, verify_message
    
class EnterpriseRunner:
    def run(self, driver, url, version, verify_data):
        checkpoint('STARTING ENTERPRISE RUNNER OPERTION')
        if verify_data == False:
            print('Sorry, self-hosted Enterprise level runner cannot be automated. Please add manually')
        op_message = f'Sorry, self-hosted enterprise level runner cannot be automated. Please add manually'
        operation_message = f'{__class__.__name__} Data - {is_skip} \n  {op_message}'
        checkpoint('OPERATION ENTERPRISE RUNNER COMPLETED')

        checkpoint("VERIFYING REPO-RUNNER DATA")
        #org runner
        driver.get(f'{url}/enterprises/github/settings/actions/runners')
        #v3.7
        try:
            runner = driver.find_element(By.CSS_SELECTOR,'.h4.color-fg-default')
            message = f'runner round on enterprise level = {runner.text} - {is_pass}'
            print(f'Enterprise Runner {runner.text} found!')
            verify_status = True
        except:
            message = f'no runner found on enterprise level. Please add runner manually - {is_fail}'
            print('No enterprise runner found.')
            verify_status = False

        if verify_status:
            v_message = f'{__class__.__name__} Data - {is_complete}'
            verify_message = f'{v_message} \n  {message}'
        else:
            verify_message = f'{__class__.__name__} Data - {is_complete} \n  {message}'
            checkpoint("REPO-RUNNER DATA VERIFICATION COMPLETED")

        return version, operation_message, verify_message
    
class OrganizationEmpty:
    """
    This testcase is to create empty organization
    """
    def run(self, driver, url, version, verify_data):
        checkpoint('STARTING EMPTY ORGANIZATION OPERATION')
        if verify_data == False:
            driver.get(f'{url}/organizations/new')
            driver.find_element(By.CSS_SELECTOR, '.form-control.js-new-organization-name.width-full.py-1').send_keys('empty')
            time.sleep(3)
            try:
                exist = driver.find_element(By.CSS_SELECTOR,'.form-control.js-new-organization-name.width-full.py-1.is-autocheck-errored')
                print(exist.text)
                op_message = f'organization \'empty\' already existed - {is_pass}'
            except:
                driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-large.signup-btn.width-full').click()
                print("Create Organization empty")
                op_message = f'Organization \'empty\' created. Please create runner manually - {is_pass}'
            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}'
        checkpoint('OPERATION EMPTY ORGANIZATION COMPLETED')
        
        checkpoint(f"VERIFYING {__class__.__name__} DATA")
        driver.get(f'{url}/empty')
        print('')
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            print(f'Organization empty not found')
            verify_status = False
        except:
            verify_status = True

        if verify_status == True:
            verify_message = f'{__class__.__name__} Data - {is_pass}'
        elif verify_status == False:
            verify_message = f'{__class__.__name__} Data - {is_fail}. Org \'empty\' not found.'

        checkpoint("EMPTY ORGANIZATION DATA VERIFICATION COMPLETED")
        return version, operation_message, verify_message

class Gist:
    def run(self, driver, url, version, verify_data):
        parts = url.split("://")
        if len(parts) == 2:
            protocol, rest = parts
            domain, *path = rest.split("/")
            gist_url = f"{protocol}://gist.{domain}{'/'.join(path)}"
            
            print(f"gist url : {gist_url}")
        else:
            print("Invalid URL format")

        checkpoint(f'Operation {__class__.__name__}')
        config = load_config()
        username = config.get('instance_setting','instance_username')
        if verify_data == False:
            #v3.7
            driver.get(gist_url)
            time.sleep(3)
            driver.find_element(By.NAME,'gist[description]').send_keys('Secret Gist Data')
            driver.find_element(By.NAME,'gist[contents][][name]').send_keys('secret_gist.md')
            driver.find_element(By.CLASS_NAME,'CodeMirror-code').send_keys('This is a secret gist data')
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,'.hx_create-pr-button.js-sync-select-menu-button.btn-primary.btn.BtnGroup-item').click()

            driver.get(gist_url)
            time.sleep(3)
            driver.find_element(By.NAME,'gist[description]').send_keys('Public Gist Data')
            driver.find_element(By.NAME,'gist[contents][][name]').send_keys('public_gist.md')
            driver.find_element(By.CLASS_NAME,'CodeMirror-code').send_keys('This is a public gist data')
            display = driver.find_element(By.CSS_SELECTOR,'.details-reset.details-overlay.select-menu.BtnGroup-parent.position-relative').click()
            time.sleep(2)
            gist_category = driver.find_elements(By.CLASS_NAME,'select-menu-item-heading')
            time.sleep(2)
            for element in gist_category:
                if element.is_displayed():
                    text_of_class_b = element.text
                else:
                    pass
                if element.text == 'Create public gist':
                    element.click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,'.hx_create-pr-button.js-sync-select-menu-button.btn-primary.btn.BtnGroup-item').click()
            op_message = f'Gist created - {is_pass}'
            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}' 
        print(operation_message)

        checkpoint(f'Verification {__class__.__name__}')
        driver.get(f"{gist_url}/{username}")
        time.sleep(3)
        try:
            driver.find_element(By.CLASS_NAME, 'font-mktg')
            verify_status = False
        except:
            verify_status = True

        if verify_status == True:
            message = []
            try:
                gist_list = driver.find_elements(By.CLASS_NAME,'gist-snippet')
                driver.find_element(By.CLASS_NAME,'gist-snippet')
                for gist in gist_list:
                    gist_user = gist.find_element(By.CSS_SELECTOR, '.d-inline-block.px-lg-2.px-0 a')
                    gist_name = gist.find_element(By.CLASS_NAME, 'css-truncate-target')
                    gist_f = f'{gist_user.text}/{gist_name.text}'
                    message.append(gist_f)
                status = True
            except:
                status = False
                message = "No Gist Data found. Please chack and add manually"
            
            if status == True:
                verify_message = f' Gist data - {is_pass} \n  {message}'
            elif status == False:
                verify_message = f'Gist Data - {is_fail} \n  {message}'
        elif verify_status == False:
            verify_message = f'Gist Data Verification - {is_fail}. Wrong Directory'

        print(verify_message)

        return version, operation_message, verify_message
    
class NewUser:
    def run(self, driver, url, version, verify_data):
        config = load_config()
        username = config.get('instance_setting','instance_username')
        password = config.get('instance_setting','instance_password')
        checkpoint(f'Operation {__class__.__name__}')
        if verify_data == False:
            driver.get(f'{url}/stafftools/users/invitations/new')
            try:
                driver.find_element(By.ID,"login_field").send_keys(username)
                driver.find_element(By.ID,"password").send_keys(password)
                driver.find_element(By.NAME,"commit").click()
            except:
                pass
            try:
                driver.find_element(By.CSS_SELECTOR,'.flash.flash-warn')
                invite = True 
            except:
                invite = False
            
            if invite:
                warn_message = f'Email is not enabled in console. Proceed with user invitation'
                # new user credentials
                driver.find_element(By.ID,'user_login').send_keys('user1')
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR,'.form-group.errored')
                    create_user = False
                except:
                    create_user = True
                
                #user1 not exist
                if create_user:
                    driver.find_element(By.ID,'user_email').send_keys('user1@ghe-test.net') 
                    #NOTE email used from template, if taken, need change
                    driver.find_element(By.CSS_SELECTOR,'.form-group .btn').click()
                    time.sleep(2)

                    # invite_message
                    message = driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-notice .px-2').text
                    invitation_url = message.split()[-1]

                    # Open a new empty tab using JavaScript
                    driver.execute_script("window.open('', '_blank');")

                    # Switch to the newly opened tab
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2)

                    # enter new user password
                    driver.get(invitation_url)
                    time.sleep(2)
                    driver.find_element(By.ID,"password").send_keys('bysTESTuser1')
                    driver.find_element(By.ID,"password_confirmation").send_keys('bysTESTuser1') #bysTESTuser1
                    driver.find_element(By.NAME,"commit").click()
                    time.sleep(3)
                    #close new tab
                    driver.close()
                    time.sleep(3)
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
                    op_message = f'New User created - {is_pass}'

                else:
                    op_message = f'User1 already existed - {is_skip}'

                driver.get(f'{url}/{name['OrganizationBasic']}/data/settings/access')
                time.sleep(2)
                try:
                    col = driver.find_element(By.CSS_SELECTOR,'.Box-row.clearfix.d-flex.flex-items-center.js-repo-access-entry.adminable .d-flex.flex-column.flex-auto.col-6 strong')
                    if col.text == 'user1':
                        collab = False
                    else:
                        collab = True
                except:
                    collab = True
                if collab:
                    try:
                        driver.find_element(By.CSS_SELECTOR,'.btn.btn-primary.mt-3')
                        add_people = driver.find_elements(By.CSS_SELECTOR,'.btn.btn-primary.mt-3')
                        for elem in add_people:
                            if elem.text == 'Add people':
                                elem.click()
                    except:
                        #if user1 already a collaborator
                        driver.find_element(By.CSS_SELECTOR,'.details-reset.details-overlay.details-overlay-dark.d-inline-block.text-left .btn.btn-sm.btn-primary')
                        add_people = driver.find_elements(By.CSS_SELECTOR,'.details-reset.details-overlay.details-overlay-dark.d-inline-block.text-left .btn.btn-sm.btn-primary')
                        for elem in add_people:
                            if elem.text == 'Add people':
                                elem.click()
                    time.sleep(1)
                    driver.find_element(By.NAME,'member').send_keys('user1')
                    time.sleep(1)
                    driver.find_element(By.ID,'repo-add-access-search-results-user').click()
                    driver.find_element(By.CSS_SELECTOR,'.css-truncate.css-truncate-overflow.btn-primary.btn.btn-block').click()
                    time.sleep(3)
                    op_access_message = f'Successfully add user1 to org {name['OrganizationBasic']} - {is_pass}'
                else:
                    op_access_message = f'User1 already a collaborator in org {name['OrganizationBasic']} - {is_pass}'

            else:
                warn_message = f'Email is enabled in console. Skipping user invitation - {is_skip}'
                op_access_message = f'Email is enabled in console. Skipping user1 collaboration - {is_skip}'

            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete}\n  {warn_message}\n  {op_message}\n  {op_access_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}'
        print(operation_message)

        checkpoint(f'Verification {__class__.__name__}')
        # check all user
        driver.get(f'{url}/stafftools/users')
        user_list = driver.find_elements(By.CSS_SELECTOR,'.table-list-item .col-3.table-list-cell.py-3 a')
        for user in user_list:
            if user.text == 'user1':
                user_found = True 
                break
        else:
            user_found = False

        if user_found == True:
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,'.Header-item.position-relative.mr-0 .Header-link').click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,'.dropdown-item.dropdown-signout').click()
            time.sleep(3)
            driver.find_element(By.ID,"login_field").send_keys('user1')
            driver.find_element(By.ID,"password").send_keys('bysTESTuser1')
            driver.find_element(By.NAME,"commit").click()
            time.sleep(3)
            try:
                login_meesage = driver.find_element(By.CLASS_NAME,'js-flash-alert')
                verify_message = f'{__class__.__name__} Data - {is_complete}\n  User1 found  - {is_pass}\n  but login user unsuccessful - {is_fail}'
            except:
                driver.get(f'{url}/{name['OrganizationBasic']}/data')
                time.sleep(2)
                try:
                    driver.find_element(By.CLASS_NAME, 'font-mktg')
                    collab_message = f'but user1 is not a collaborator in org {name['OrganizationBasic']} - {is_fail}'
                except:
                    collab_message = f'and user1 is a collaborator in org {name['OrganizationBasic']} - {is_pass}'
                verify_message = f'{__class__.__name__} Data - {is_complete}. \n  User1 found - {is_pass}\n  successfully login user1 - {is_pass}\n  {collab_message}'

        else:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. \n  No user1 found - {is_fail}'

        print(verify_message)

        return version, operation_message, verify_message
    
class TestEmail:
    def run(self, driver, url, version, verify_data):
        config = load_config()
        password = config.get('instance_setting','instance_password')
        checkpoint(f'Operation {__class__.__name__}')
        if verify_data == False:
            op = True
            try: #check if current is user1
                driver.get(f'{url}')
                driver.find_element(By.CSS_SELECTOR,'.Header-item.position-relative.mr-0 .Header-link').click()
                time.sleep(3)
                user = driver.find_element(By.CSS_SELECTOR,'.header-nav-current-user.css-truncate .css-truncate-target')
                if user.text == 'user1':
                    signout = False 
                    login = False
                elif user.text == 'ghe-admin':
                    signout = True
                    login = True
            except:
                signout = False
                login = True

            if signout == True:
                driver.find_element(By.CSS_SELECTOR,'.dropdown-item.dropdown-signout').click()
                time.sleep(3)

            if login == True:
                driver.find_element(By.ID,"login_field").send_keys('user1')
                driver.find_element(By.ID,"password").send_keys('bysTESTuser1')
                driver.find_element(By.NAME,"commit").click()
                try:
                    incorrect = driver.find_element(By.CSS_SELECTOR,'.flash.flash-full.flash-error .px-2')
                    op = False
                except:
                    op = True

            if op == True:
                driver.get(f'{url}/{name['OrganizationBasic']}/data/issues')
                time.sleep(3)
                issue_open = driver.find_elements(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative .flex-auto.min-width-0.p-2.pr-3.pr-md-2 .Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
                for elem in issue_open:
                    if elem.text == 'Sample Open Issue':
                        elem.click()
                        time.sleep(2)
                        comment = True
                        break
                else:
                    comment = False

                if comment:
                    driver.find_element(By.ID,'new_comment_field').send_keys('Test user1 comment')
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR,'.color-bg-subtle.ml-1 .btn-primary.btn').click()
                    op_message = f'User1 commented on issue - {is_pass}'
                else:
                    op_message = f'sample open issue not found. Unable to comment - {is_fail}'
            else:
                op_message = f'User1 not exist - {is_fail}'

            operation = True
        else:
            operation = False

        if operation:
            operation_message = f'{__class__.__name__} Data - {is_complete} \n  {op_message}'
        else:
            operation_message = f'{__class__.__name__} Data - {is_skip}'
        print(operation_message)

        checkpoint(f'Verification {__class__.__name__}')
        try: #check if current is user1
            driver.find_element(By.ID,"login_field").send_keys('ghe-admin')
            driver.find_element(By.ID,"password").send_keys(password)
            driver.find_element(By.NAME,"commit").click()
            time.sleep(3)
            login = False
            sign_out = False
        except:
            login = True
            sign_out = True
        
        if login == True:
            driver.get(f'{url}')
            driver.find_element(By.CSS_SELECTOR,'.Header-item.position-relative.mr-0 .Header-link').click()
            time.sleep(2)
            user = driver.find_element(By.CSS_SELECTOR,'.header-nav-current-user.css-truncate .css-truncate-target')
            if user.text == 'ghe-admin':
                sign_out = False
            else:
                sign_out = False

        #tak guna pun
        if sign_out == True:
            driver.find_element(By.CSS_SELECTOR,'.Header-item.position-relative.mr-0.d-none.d-md-flex .Header-link').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,'.dropdown-item.dropdown-signout').click()
            time.sleep(5)
            driver.find_element(By.ID,"login_field").send_keys('ghe-admin')
            driver.find_element(By.ID,"password").send_keys(password)
            driver.find_element(By.NAME,"commit").click()
            time.sleep(3)
        
        # check email comment
        driver.get(f'{url}/{name['OrganizationBasic']}/data/issues')
        time.sleep(3)
        issue_open = driver.find_elements(By.CSS_SELECTOR,'.d-flex.Box-row--drag-hide.position-relative .flex-auto.min-width-0.p-2.pr-3.pr-md-2 .Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
        for elem in issue_open:
            if elem.text == 'Sample Open Issue':
                elem.click()
                time.sleep(2)
                vcomment = True
                break
        else:
            vcomment = False
        
        if vcomment: #author Link--primary text-bold css-overflow-wrap-anywhere 
            user_comment = driver.find_elements(By.CSS_SELECTOR,'.author.Link--primary.text-bold.css-overflow-wrap-anywhere')
            for user in user_comment:
                if user.text == 'user1':
                    verify_status = True
                    break
            else:
                verify_status = False 
        else:
            verify_status = False
        
        if verify_status == True:
            verify_message = f'{__class__.__name__} Data - {is_pass}. User1 commented on this issue. Please reply to this comment from github email.'
        elif verify_status == False:
            verify_message = f'{__class__.__name__} Data - {is_fail}. No comment found from user1. Please add comment from user1'

        print(verify_message)

        return version, operation_message, verify_message
    
class ManagementConsoleSetting:
    """
    Checks management console setting [Email, Chat Integration, dependency graph, actions, packages]
    """
    def run(self, driver, url, version, verify_data):
        config = load_config()
        password = config.get('instance_setting','instance_password')
        checkpoint(f'Operation {__class__.__name__}')
        if verify_data == False:
            print(f'Operation {__class__.__name__} cannot be automted. Please add manually')
            vr = False
        operation_message  = f'{__class__.__name__} cannot be automated. Please add manually - {is_complete}'
        print(operation_message)
        
        checkpoint(f'Verification {__class__.__name__}')
        driver.get(f'{url}/setup/settings')
        time.sleep(3)
        try:
            driver.find_element(By.NAME,'password').send_keys(password)
            driver.find_element(By.CSS_SELECTOR,'.btn.btn-primary.continue-install.js-upload-license').click()
            time.sleep(3)
        except:
            pass

        page = driver.find_element(By.CSS_SELECTOR,'.page-main-header.js-page-main-header h1')
        if page.text == 'Settings':
            message = 'Successfully logged in to Management Console Settings page'
            verify_status = True
        elif page.text == 'Authentication Required':
            message = 'Unable to login Management Console. Please ensure your password is correct.'
            verify_status = False
        else:
            message = "Successfully logged in to Management Console, but not in Settings page"
            driver.get(f'{url}/setup/settings')
            verify_status = True  

        if verify_status == True:
            #check if cluster
            try:
                display_text = driver.find_element(By.CSS_SELECTOR,'.page-settings .blankslate h2')
                if display_text.text == 'Disabled in Cluster':
                    cluster = True
            except:
                cluster = False

            if cluster == False:
                cluster_message = f'Instance is not in cluster. Proceed Verification'
                #email
                email = driver.find_element(By.ID,'email')
                try:
                    email.find_element(By.CSS_SELECTOR,'.checkbox-item.active')
                    # email_active = True
                    email_message = f'Email enabled! - {is_pass}'
                except:
                    # email_active = False
                    email_message = f'Email is not enabled. Please enable manually. - {is_fail}'
                
                #actions
                action = driver.find_element(By.ID,'actions')
                try:
                    action.find_element(By.CSS_SELECTOR,'.checkbox-item.active')
                    action_message = f'Actions enabled! - {is_pass}'
                except:
                    action_message = f'Actions is not enabled. Please enable manually. - {is_fail}'

                #packages
                package = driver.find_element(By.ID,'packages')
                try:
                    package.find_element(By.CSS_SELECTOR,'.checkbox-item.active')
                    package_message = f'Packages enabled! - {is_pass}'
                except:
                    package_message = f'Packages is not enabled. Please enable manually. - {is_fail}'

                #dependency graph 
                security = driver.find_element(By.ID,'security')
                try:
                    security.find_element(By.CSS_SELECTOR,'.checkbox-item.js-enable-dependency-graph-toggle.active')
                    security_message = f'Dependency Graph enabled! - {is_pass}'
                except:
                    security_message = f'Dependency Graph is not enabled. Please enable manually. - {is_fail}'

                #v3.11 #TODO what version?
                chat_message = f'Chat integration is not available for version {version} - {is_pass}'

            else:
                cluster_message = f'Instance is in cluster. Aborting Verification'
        
        if verify_status == True:
            if cluster == False:
                verify_message = f'{__class__.__name__} Data - {is_complete}\n  {cluster_message}\n  {email_message} \n  {action_message} \n  {package_message} \n  {security_message} \n  {chat_message}'
            else:
                verify_message = f'{__class__.__name__} Data - {is_incomplete}\n  {cluster_message}'
        elif verify_status == False:
            verify_message = f'{__class__.__name__} Data - {is_incomplete}. {message}'

        print(verify_message)

        return version, operation_message, verify_message
    
class testdebug:
    def run(self, driver, url, version, verify_data):
        config = load_config()
        password = config.get('instance_setting','instance_password')
        print(password)
        verify_message = 'hehe'
        operation_message = 'huhu'
        return version, operation_message, verify_message