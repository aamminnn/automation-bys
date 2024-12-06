import argparse
import configparser
from controller import Controller 
import time
from prettytable import PrettyTable
from testcase import testcase

config = configparser.ConfigParser()
with open("config.ini","r") as file_object:
    config.read_file(file_object)
default_url = config.get('instance_setting','instance_url')
default_username = config.get('instance_setting','instance_username')
default_password = config.get('instance_setting','instance_password')
operation_summary_title= f'\n\033[33m------------DATA OPERATION SUMMARY--------------\033[0m' # yellow
verification_summary_title = f'\n\033[33m------------DATA VERIFICATION SUMMARY--------------\033[0m' # yellow
table_summary_title = f'\n\033[33m--TABLE SUMMARY--\033[0m' # yellow
instance_summary_title = f'\n\033[33m------------TESTCASE SUMMARY--------------\033[0m' # yellow

def update_config(var, item):
    config = configparser.ConfigParser()
    with open("config.ini","r") as file_object:
        config.read_file(file_object)
    # config.read('config.ini')

    # Update the values based on user input
    config['instance_setting'][item] = var

    # Save the changes back to the config file
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def run(url:str, password:str, verify_data:bool, values_list=None):
    table = PrettyTable()
    # table.clear()
    #count runtime
    start_time = time.time()

    # Access the values
    if url.endswith('/'):
        # Remove backslash
        url = url.rstrip('/')
        update_config(url,'instance_url')

    password = password
    update_config(password,'instance_password')

    # logic
    print(f"Instance url: {url}") 
    print(f"instance username: {default_username}")
    print(f"instance password: {password}")
    print(f"Running automation script on {url} as {default_username}")

    if values_list:
        print(f"Running automation script on {values_list} testcases")

    else:
        print("Running all testcases")

    tc = Controller(url)

    try:
        tc.open_chrome()
        print(f"Open {url} using Google Chrome!")
    except Exception as e:
        print(f"Fail to open {url}. Error in {__file__}. {e}")

    try:
        tc.sign_in(default_username, password)
        print(f"Successfully log in {default_username}")
    except Exception as e:
        print(f"Fail to sign in {default_username}. Error in {__file__}. {e}")

    for trial in range(3):
        try:
            version = tc.get_version()
            break
        except Exception as e:
            print(f"Fail to get instance version. Error in {__file__}. {e}")

    try:
        version, operation_summary_list, verification_summary_list, table_testcase, table_result= tc.execute_testcase(version, values_list, verify_data)
        if values_list == None:
            print("Successfully executed all testcases")
        else:
            print(f"Successfuly executed {values_list} testcases")
    except Exception as e:
        print(f"Fail to execute testcase operations. Error in {__file__}. {e}")

    print(instance_summary_title)
    try:
        tc.instance_summary(version)
    except:
        print('Cannot find instance summary')

    print(operation_summary_title)
    try:
        tc.testcase_summary(operation_summary_list)
    except:
        print("Cannot find testcase summary")

    print(verification_summary_title)
    try:
        tc.verification_summary(verification_summary_list)
    except:
        print("Cannot Verify Data")

    print(table_summary_title)
    try:
        table.field_names = ["Testcase","Result"]
        for i in range(len(table_testcase)):
            table.add_row([table_testcase[i], table_result[i]])
        print(table)
    except:
        print('Cannot Produce Table Summary')

    try:
        tc.quit_chrome()
        print('Quitting Chrome...')
    except Exception as e:
        print(f'Chrome is not open. Error in {__file__}. {e}')

    end_time = time.time()
    elapsed_time = end_time - start_time
    # print(f"\nProgram runtime: {elapsed_time:.2f} seconds")
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"\nProgram runtime: {int(minutes)} minutes {seconds:.2f} seconds")

    return version, operation_summary_list, verification_summary_list, table



# if __name__ == '__main__':
#     run()

