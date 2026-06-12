import os

env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

from modules.integrations.telegram_bot import start_bot, bot_status
import time

print(start_bot())
time.sleep(2)
print(bot_status())
print("Bot running. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping...")
