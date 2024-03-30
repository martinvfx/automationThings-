from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import string , keyboard, pyperclip

# Set the URL to website images
base_url = "https://qudosbankarena.com.au/wp-content/uploads/2023/05/QBA-Seats-"
download_dir = "%userprofile%\downloads\downloaded_images" #  place to drop the images.
download_dir = os.path.expandvars(download_dir)
# print(download_dir)

# Function to generate URLs with different numbers and names
def generate_urls():
    # sections = ["Lower", "Upper", ["Floor_" + L for L in list(string.ascii_uppercase)[:8]], "Suites", "Middle"]
    sections = ["Lower", "Upper", "Suites", "Middle"] + ["Floor_" + L for L in list(string.ascii_uppercase)[:8]] #the end word after number in jpg file.

    for i in range(1, 100):
        for section in sections:
            if "Floor_" in section: # To prevent call "Floor" multiple times.
                print(f"\n\t section is = {section}")
                yield f"{base_url}{section}.jpg"
            else:
                if isinstance(section, list):
                    for sub_section in section:
                        yield f"{base_url}{sub_section}_{i}.jpg"
                else:
                    yield f"{base_url}{section}_{i}.jpg"


# Function to open URLs using Selenium and save images
def open_and_save_images(download_dir):
    # Create directory if not exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Initialize Chrome WebDriver
    # driver = webdriver.Chrome()

    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    # Loop through generated URLs
    for url in generate_urls():
        try:

            # Open the URL
            driver.get(url)
            print("Opened URL:", url)

            # Wait for the image to load completely
            image_element = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.TAG_NAME, 'img')))

            # Right-click on the image to trigger the context menu
            # ActionChains(driver).context_click(driver.find_element_by_tag_name('img')).perform()
            # Focus on the image element (might be necessary for keyboard shortcuts)
            actions = webdriver.ActionChains(driver)
            time.sleep(1)  # Short pause for focus transfer
            actions.move_to_element(image_element).perform()

            saved_image_path = os.path.join(download_dir, os.path.basename(url))

            # time.sleep(1)  # Wait for the context menu to appear
            if not os.path.exists(saved_image_path):

                keyboard.press(['ctrl', 's'])
                time.sleep(0.5)
                keyboard.release('s')
                keyboard.release('ctrl')
                time.sleep(0.5)
                for t in range(6): # press Tab key to swith into path text box.
                    keyboard.press('Tab')
                    time.sleep(0.2)
                keyboard.press_and_release ('enter')
                # time.sleep(1)
                pyperclip.copy(download_dir) # Send download dir to clipboard.
                keyboard.press('Control+v')
                keyboard.press_and_release ('enter')
                keyboard.release('ctrl')
                for p in range(9):
                    keyboard.press_and_release  ('Tab')
                    time.sleep(0.2)
                keyboard.press_and_release('alt+s')
                time.sleep(0.5)
                keyboard.press_and_release ('y')
                keyboard.press_and_release ('enter')
                # Check if the image is saved in the download directory
                if os.path.exists(saved_image_path):
                    print("Image saved successfully:", saved_image_path)
                else:
                    print("Error: Image not saved", saved_image_path)

            else:
                print("Image is already downloaded in: ", saved_image_path)

            # Wait for a short time before proceeding to the next URL
            time.sleep(2)
            driver.switch_to.window(driver.current_window_handles)
            # driver.switch_to.window(driver.window_handles[-1])

        except Exception as e:
            print("Error:", e)

    # Close the WebDriver session
    driver.quit()


if __name__ == "__main__":
    open_and_save_images(download_dir)
