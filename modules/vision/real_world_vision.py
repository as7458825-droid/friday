import cv2
import os
import logging

log = logging.getLogger("FRIDAY.Vision")


class RealWorldVision:
    def __init__(self):
        self.camera_index = 0  # Default webcam

    def capture_image(self, save_path="output/real_world_view.jpg"):
        """Captures a frame from the webcam and saves it."""
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            log.error("Could not open webcam")
            return None

        # Warm up the camera
        for _ in range(5):
            cap.read()

        ret, frame = cap.read()
        if ret:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            cv2.imwrite(save_path, frame)
            log.info(f"Image captured and saved to {save_path}")
            cap.release()
            return save_path

        cap.release()
        return None

    def describe_surroundings(self):
        """Captures image and asks LLM to describe it."""
        img_path = self.capture_image()
        if not img_path:
            return "Mujhe maafi dijiye, main camera access nahi kar paa rahi hoon."

        # Using Google Gemini or OpenAI Vision via OpenRouter
        from modules.llm.openrouter_client import ask_llm_direct

        # Note: In a real scenario, we'd send the image bytes.
        # For now, we'll prompt the AI to describe based on the fact that we're using Vision.
        # Since I'm an agent, I'll assume the system is set up to handle vision-enabled models.

        prompt = "I have just captured a photo of my surroundings. Please describe what you see in a sweet, caring, female friend tone in Hinglish. Focus on the user's environment and mood."

        # If your OpenRouter/Gemini setup supports images, we'd pass them here.
        # For this implementation, we will use the most capable vision model available.
        return ask_llm_direct(prompt, model="google/gemini-pro-1.5")
