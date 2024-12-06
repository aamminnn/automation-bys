import webbrowser
import requests
import io
import zipfile
import re



# Function to get live stock data for a symbol
def get_api():
	url = f"https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
	response = requests.get(url)
	
	# Check if the response is successful
	if response.status_code == 200:
		data = response.json()
		chromedriver = data["channels"]["Stable"]["downloads"]["chromedriver"][2]["url"]
		return chromedriver
	else:
		return None

# api = get_api()

def extract_chromedriver(api):
	response = requests.get(api)
		
	if response.status_code == 200:
		# Create a file-like object from the response content
		zip_file = io.BytesIO(response.content)

		# Create a ZipFile object from the file-like object
		with zipfile.ZipFile(zip_file, 'r') as zip_ref:
			# Extract all contents of the ZIP file
			zip_ref.extractall('.')

		print("ZIP file downloaded and extracted successfully")
		# 3) Check extracted driver version
		driver_version = re.search(r'\d+', api).group()
		print("Extracted ChromeDriver Version:", driver_version)
	else:
		print("Failed to download ZIP file from the URL:", response.status_code)

	
