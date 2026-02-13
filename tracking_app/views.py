from django.shortcuts import render
from .models import MouseClick, MouseMovement
from .models import KeyPress
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractWeek
from django.db.models import Count, F, ExpressionWrapper, fields



import json

def main_page(request):
    return render(request, 'tracking_app/main.html')

from django.shortcuts import render
from .models import MouseClick, MouseMovement
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import json

from django.shortcuts import render
from .models import MouseClick, MouseMovement
from django.db.models import Count
import json
from datetime import datetime

def dashboard(request):
    # Get the start and end dates from the request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Filter mouse clicks and movements by the selected date range
    mouse_clicks = MouseClick.objects.all()
    mouse_movements = MouseMovement.objects.all()

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        mouse_clicks = mouse_clicks.filter(timestamp__date__range=[start_date, end_date])
        mouse_movements = mouse_movements.filter(timestamp__date__range=[start_date, end_date])

    # Screen resolution (adjust to your screen size)
    screen_width = 1920
    screen_height = 1080

    # Heatmap container size (adjust to your desired size)
    heatmap_width = 960  # Half of screen width
    heatmap_height = 540  # Half of screen height

    # Normalize mouse click data
    mouse_click_data = [
        {
            "x": int((click.x / screen_width) * heatmap_width),
            "y": int((click.y / screen_height) * heatmap_height),
            "value": 1
        }
        for click in mouse_clicks
    ]

    # Normalize mouse movement data
    mouse_movement_data = [
        {
            "x": int((movement.x / screen_width) * heatmap_width),
            "y": int((movement.y / screen_height) * heatmap_height),
            "value": 1
        }
        for movement in mouse_movements
    ]

    # Calculate click frequency by button
    mouse_button_clicks = mouse_clicks.values('button').annotate(count=Count('button')).order_by('button')
    mouse_button_clicks_dict = {item['button']: item['count'] for item in mouse_button_clicks}

    # Default to 0 for all buttons
    mouse_button_clicks_data = [
        mouse_button_clicks_dict.get('Button.left', 0),
        mouse_button_clicks_dict.get('Button.right', 0),
        mouse_button_clicks_dict.get('Button.middle', 0),
    ]

    context = {
        'mouse_click_data': json.dumps(mouse_click_data),
        'mouse_movement_data': json.dumps(mouse_movement_data),
        'mouse_button_clicks': json.dumps(mouse_button_clicks_data),
        'heatmap_width': heatmap_width,
        'heatmap_height': heatmap_height,
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
    }
    return render(request, 'tracking_app/dashboard.html', context)



def key_dashboard(request):
    # Get the start and end dates from the request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Filter key presses by the selected date range
    key_presses = KeyPress.objects.all()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        key_presses = key_presses.filter(timestamp__date__range=[start_date, end_date])

    # Aggregate key press counts
    key_press_counts = key_presses.values('key').annotate(count=Count('key')).order_by('key')
    key_press_counts_dict = {item['key']: item['count'] for item in key_press_counts}

    # Aggregate key presses by day of the week
    key_presses_by_day = key_presses.annotate(
        day_of_week=ExtractWeekDay('timestamp')  # Extract day of the week (1=Sunday, 7=Saturday)
    ).values('day_of_week').annotate(count=Count('id')).order_by('day_of_week')

    # Map day numbers to day names
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    key_presses_by_day_dict = {
        day_names[item['day_of_week'] - 1]: item['count'] for item in key_presses_by_day
    }

    # Typing Pattern Analysis
    # Calculate typing speed (characters per minute)
    total_key_presses = key_presses.count()
    if total_key_presses > 1:
        first_press = key_presses.first().timestamp
        last_press = key_presses.last().timestamp
        total_time = (last_press - first_press).total_seconds() / 60  # Total time in minutes
        typing_speed = total_key_presses / total_time  # Characters per minute
    else:
        typing_speed = 0

    # Calculate common key combinations (e.g., "Ctrl+C")
    key_combinations = key_presses.annotate(
        next_key=F('key'),
        next_timestamp=F('timestamp')
    ).values('key', 'next_key', 'next_timestamp').order_by('timestamp')

    common_combinations = {}
    for i in range(len(key_combinations) - 1):
        current = key_combinations[i]
        next_item = key_combinations[i + 1]
        combination = f"{current['key']}+{next_item['key']}"
        if combination in common_combinations:
            common_combinations[combination] += 1
        else:
            common_combinations[combination] = 1

    # Sort common combinations by frequency
    common_combinations = dict(sorted(common_combinations.items(), key=lambda item: item[1], reverse=True)[:5])

    # Calculate key press intervals
    key_intervals = []
    for i in range(len(key_presses) - 1):
        current = key_presses[i].timestamp
        next_item = key_presses[i + 1].timestamp
        interval = (next_item - current).total_seconds()  # Interval in seconds
        key_intervals.append(interval)

    average_interval = sum(key_intervals) / len(key_intervals) if key_intervals else 0

    # Pass the data to the template
    context = {
        'key_press_counts': json.dumps(key_press_counts_dict),
        'key_presses_by_day': json.dumps(key_presses_by_day_dict),
        'typing_speed': typing_speed,
        'common_combinations': json.dumps(common_combinations),
        'average_interval': average_interval,
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
    }
    return render(request, 'tracking_app/keyboard_heatmap_usage.html', context)
