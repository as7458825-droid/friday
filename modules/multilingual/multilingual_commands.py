# Re-export everything from commands_multilingual
from modules.multilingual.commands_multilingual import *
try:
    from modules.multilingual.commands_multilingual import match_multilingual_command
except ImportError:
    def match_multilingual_command(text: str):
        return None
