import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from streamlit_ui import get_selected_sp, trigger_download, notify_completion
from log_collections.capture_console_logs import CaptureConsoleLogs

# Set up logger
LOGGER = CaptureConsoleLogs.get_logger()

def create_folder_sp(sp_name):
    """Create a folder for the selected SP name."""
    base_dir = r"D:\project\Python_practice\aihubmodeldownload"
    new_dir_path = os.path.join(base_dir, sp_name)

    # Create the new directory
    try:
        os.makedirs(new_dir_path)
        LOGGER.info(f"Directory '{new_dir_path}' created successfully.")
    except FileExistsError:
        LOGGER.info(f"Directory '{new_dir_path}' already exists.")
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
    return new_dir_path

def main():
    # Streamlit UI interaction
    selected_sp_name, confirmed = get_selected_sp()

    if not confirmed:
        return  # Wait for user confirmation

    # Create a folder for the selected SP
    final_dir = create_folder_sp(selected_sp_name)

    # Set up Edge WebDriver
    edge_driver_path = r"D:\project\Python_practice\edgedriver_win64\msedgedriver.exe"
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.prompt_for_download": False,
        "download.default_directory": final_dir,
        "directory_upgrade": True
    }
    edge_options.add_experimental_option("prefs", prefs)
    service = EdgeService(edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        # Start downloading if the button is clicked
        if trigger_download():
            LOGGER.info("Starting download process...")

            # Example: Call your download logic here
            # driver.get("https://aihub.qualcomm.com/")
            # Your Selenium-based download logic...

            notify_completion(success=True, message="Download process completed successfully!")
    except Exception as e:
        LOGGER.error(f"Error during download: {e}")
        notify_completion(success=False, message=f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
