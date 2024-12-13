import streamlit as st
from log_collections.capture_console_logs import CaptureConsoleLogs

# Set up logger
LOGGER = CaptureConsoleLogs.get_logger()

def get_selected_sp():
    """Create a Streamlit UI for selecting SP name and confirming selection."""
    # Streamlit UI
    st.title("Qualcomm Model Downloader")
    st.sidebar.header("Model Selection")

    # Dropdown for selecting SP name
    sp_names = ["SA8650P", "SA8775P", "QCS6490"]
    selected_sp_name = st.sidebar.selectbox("Select a SP name", sp_names)

    # Show the selected SP name in the main app
    st.write(f"Selected SP: {selected_sp_name}")

    # Streamlit button for confirmation
    confirmed = st.sidebar.button("Confirm Selection")

    # Log and return the result
    if confirmed:
        LOGGER.info(f"User confirmed SP selection: {selected_sp_name}")
        st.success(f"SP '{selected_sp_name}' confirmed.")
    return selected_sp_name, confirmed

def trigger_download():
    """Add UI components to start the download process."""
    # Add interactive control to trigger downloading
    start_download = st.sidebar.button("Start Download")
    if start_download:
        st.write("Starting the download process...")
    return start_download

def notify_completion(success=True, message=""):
    """Notify the user about the completion status."""
    if success:
        st.success(message)
    else:
        st.error(message)
