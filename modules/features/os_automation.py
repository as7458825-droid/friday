import pyautogui
import os
import logging

logger = logging.getLogger(__name__)


class OSAutomation:
    """Advanced System & Application Automation for FRIDAY"""

    def open_app(self, app_name):
        """Attempts to open an application by name"""
        try:
            # Simple mapping for demo
            apps = {
                "notepad": "notepad.exe",
                "calc": "calc.exe",
                "chrome": "chrome.exe",
            }
            exe = apps.get(app_name.lower(), app_name)
            os.startfile(exe)
            return f"Opening {app_name}..."
        except Exception as e:
            return f"OS Automation Error: {e}"

    def take_screenshot(self, filename="screenshot.png"):
        """Captures the entire screen"""
        try:
            pyautogui.screenshot(filename)
            return f"Screenshot saved as {filename}."
        except Exception as e:
            return f"Screenshot Error: {e}"


def os_update(command):
    oa = OSAutomation()
    if "open" in command:
        app = command.split("open")[-1].strip()
        return oa.open_app(app)
    if "screenshot" in command:
        return oa.take_screenshot()
    return "OS Automation online. Commands: open [app], screenshot."
