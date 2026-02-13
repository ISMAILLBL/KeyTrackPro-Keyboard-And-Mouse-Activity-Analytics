import os
import sys
from pynput import keyboard, mouse
from django.utils import timezone

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracking_project.settings')

# Initialize Django
import django
django.setup()

# Import your models
from tracking_app.models import KeyPress, MouseClick, MouseMovement, KeyCombination

# Keyboard event handler
def on_key_press(key):
    try:
        KeyPress.objects.create(key=key.char)
    except AttributeError:
        KeyPress.objects.create(key=str(key))

# Mouse click event handler
def on_mouse_click(x, y, button, pressed):
    if pressed:
        MouseClick.objects.create(button=str(button), x=x, y=y)

# Mouse movement event handler
def on_mouse_move(x, y):
    MouseMovement.objects.create(x=x, y=y)

# Start the listeners
with keyboard.Listener(on_press=on_key_press) as keyboard_listener:
    with mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()

