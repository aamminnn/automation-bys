# automation_script
## Python Installation Steps (Terminal)
1. Install Homebrew `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` (Can skip this step).
2. Install Python3 `brew install python`.
3. Check python3 version with `python3 --version`.

## Library and Modules installation
1. Git clone `automation_dataset`repo.
2. **Creating Virtual Environment**  
- Create virtual environment by running `python3 -m venv venv`
- Activate the virtual environment by running `source venv/bin/activate`
- If virtual environment is activated, your terminal should have your virtual environment displayed in bracket. e.g:`(venv) path/to/your/macbook%`
3. **Installing Selenium Modules**  
- Once virutal environment activated, Install Selenium with `pip install selenium`.
- Check Selenium Version `pip show selenium`.
- “chromedriver” cannot be opened because the developer cannot be verified.
- Setting -> privacy and security -> security tap -> allow anyway
- [optional] macOS cannot verify the developer of “chromedriver”. Are you sure you want to open it? `-Open`
4. **Installing requests Module**
  - Inside virtual environment, install requests module by running `pip install requests`
5. **Installing prettytable Modules**  
- Inside virtual environment, install prettytable by running  `pip install prettytable`.

## IMPORTANT
1. Only Modify `script.py` based on needs.
2. #### Do Not Merge/make changes into `main` Branch without approval. Any changes please create a Pull Request First!

## Documentation
1. Inside documentation folder contain `release-notes` which shows latest updates accross all version
2. Also, documentation folder will contain any documentation related to automation such as `Testcase-Script.pdf` which shows detailed steps for each testcase.
3. It is recommended to document the test steps inside `Testcase-Script.pdf` before writing testcase script.

## Running the script
1. git clone this repo to local.
2. If selenium not installed, please installed first refer to steps above.
3. To do Data Operation, run `python3 run.py -u <url> -p <password>`.  
4. To do Data Verification, run `python3 run.py -u <url> -p <password> -v`.  
5. In case you need to run specific testcase (for example RepoData and Wiki), include `-l RepoData Wiki ` in your run command.  
6. Url and password will be automatically saved in `config.ini` file.

## Using User Interface (Working In Progress)
1. git clone this repo to local.  
2. run `python3 main.py`.  
3. Insert instance url and password.  
4. Tick testcase. (Required).  
5. Click run to add data. Click verify to verify data.  
6. UI wont exit after run, so no need to run command everytime, just reuse the UI.  

## About automation script
1. Script contains Data Operation and Data Verification for every version from `3.7.0` - `3.14.0`.  
Data Operation handle he addition of standardize data into the instance. Data Operation automatically include Data Verification.  
Data Verification verify if the standardize data is present in the instance. Data verification will exclude Data Operation.  
2. Flaws:  
- Runner-related operation cannot be automated.  
- Cloning-related operation cannot be automated.  

## Script setup (Current. Will be updated from time to time)
1. git clone this repo to local.
2. `cd` to this cloned folder.
3. Any new testcase created in `script.py` need to be added in `testcase.py`

## Modifying a script
1. In your cloned folder, run `git branch` and ensure you are in `main` branch. run `git pull`. This will fetch latest updates.
2. run `git checkout -b <new_branch_name>`. This will be your working branch. not `main` branch.
3. Modify your testcase script
4. To push your changes, run `git add .`
5. run `git commit -m 'commit message'`
6. run `git push origin <new_branch_name>` (same as working branch)
7. In github repo, create a pull request but **don't merge!**
