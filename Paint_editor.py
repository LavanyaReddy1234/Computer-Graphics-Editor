import cv2
import numpy as np
import sys

# Global variables for the landing page
landing_buttons = []
button_width, button_height = 250, 50
button_margin = 20
button_radius = 10

# Function to draw flat buttons with shadow
def draw_stylish_button(img, x, y, width, height, radius, label):
    # Draw button shadow
    shadow_color = (150, 150, 150)
    shadow_offset = 5
    cv2.rectangle(img, (x + shadow_offset, y + shadow_offset), (x + width + shadow_offset, y + height + shadow_offset), shadow_color, -1)

    # Draw button background
    button_color = (70, 130, 180)  # Steel blue color
    cv2.rectangle(img, (x, y), (x + width, y + height), button_color, -1, cv2.LINE_AA)

    # Draw button border
    border_color = (0, 0, 0)
    cv2.rectangle(img, (x, y), (x + width, y + height), border_color, 2, cv2.LINE_AA)

    # Draw button label
    text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    text_x = x + (width - text_size[0]) // 2
    text_y = y + (height + text_size[1]) // 2 - 5
    cv2.putText(img, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

# Function to handle landing page actions
def handle_landing_action(action):
    global running
    print(f"Button clicked: {action}")  # Debugging line
    if action == 'Start Paint Editor':
        running = False
    elif action == 'Exit':
        cv2.destroyAllWindows()
        sys.exit()

# Function to display buttons on the landing page
def display_landing_buttons(canvas):
    num_buttons = len(landing_buttons)
    button_x_start = (canvas.shape[1] - button_width) // 2
    button_y_start = (canvas.shape[0] - button_height * num_buttons - button_margin * (num_buttons - 1)) // 2

    for i, button in enumerate(landing_buttons):
        x = button_x_start
        y = button_y_start + i * (button_height + button_margin)
        button['pos'] = (x, y)  # Set button position
        draw_stylish_button(canvas, x, y, button_width, button_height, button_radius, button['label'])

# Function to handle mouse events on the landing page
def landing_page_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for button in landing_buttons:
            bx, by = button['pos']
            if bx <= x <= bx + button_width and by <= y <= by + button_height:
                handle_landing_action(button['label'])
                return  # Exit after handling the click

# Function to initialize and show the landing page
def show_landing_page():
    global running, landing_buttons
    running = True

    landing_window_height, landing_window_width = 500, 600
    landing_canvas = np.ones((landing_window_height, landing_window_width, 3), dtype='uint8') * 255

    # Create a gradient background
    for i in range(landing_window_height):
        color = (255 - int(255 * (i / landing_window_height)), 200, 150)
        cv2.line(landing_canvas, (0, i), (landing_window_width, i), color, 1)

    # Add a welcome note
    welcome_text = "Welcome to the Paint Editor!"
    text_size, _ = cv2.getTextSize(welcome_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)
    text_x = (landing_window_width - text_size[0]) // 2
    text_y = 100
    cv2.putText(landing_canvas, welcome_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2, cv2.LINE_AA)

    # Button configuration for landing page
    landing_buttons = [
        {'label': 'Start Paint Editor', 'pos': (0, 0)},  # Position will be adjusted in display_landing_buttons()
        {'label': 'Exit', 'pos': (0, 0)}  # Position will be adjusted in display_landing_buttons()
    ]

    # Bind the landing page event function to mouse events
    cv2.namedWindow('Landing Page')
    cv2.setMouseCallback('Landing Page', landing_page_event)

    while running:
        display_landing_canvas = landing_canvas.copy()
        display_landing_buttons(display_landing_canvas)
        cv2.imshow('Landing Page', display_landing_canvas)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC key to exit from landing page
            cv2.destroyAllWindows()
            sys.exit()

    cv2.destroyAllWindows()
    start_paint_editor()

# Function to initialize the paint editor
def start_paint_editor():
    # Initialize a blank canvas
    window_height, window_width = 900, 1200
    canvas = np.ones((window_height, window_width, 3), dtype='uint8') * 255

    # Initialize drawing variables
    drawing = False
    brush_size = 4
    pen_size = 3  # Pen size
    color = (0, 0, 0)  # Black color
    shape = None  # No shape selected initially
    x1, y1 = 0, 0
    line_start = None

    # Create window and bind the draw function to mouse events
    cv2.namedWindow('Paint')

    # Color palette
    colors = {
        'black': (0, 0, 0),
        'red': (0, 0, 255),
        'green': (0, 255, 0),
        'blue': (255, 0, 0),
        'yellow': (0, 255, 255),
        'white': (255, 255, 255),
        'pink': (125,125,125)
    }

    # Button configuration
    button_width, button_height = 80, 30
    button_margin = 8
    button_radius = 5

    buttons = [
        {'label': 'Clear', 'pos': (button_margin, button_margin)},
        {'label': 'Black', 'pos': (button_margin + button_width + button_margin, button_margin)},
        {'label': 'Red', 'pos': (button_margin + 2 * (button_width + button_margin), button_margin)},
        {'label': 'Green', 'pos': (button_margin + 3 * (button_width + button_margin), button_margin)},
        {'label': 'Blue', 'pos': (button_margin + 4 * (button_width + button_margin), button_margin)},
        {'label': 'Yellow', 'pos': (button_margin + 5 * (button_width + button_margin), button_margin)},
        {'label': 'pink', 'pos': (button_margin + 6 * (button_width + button_margin), button_margin)},
        {'label': 'Eraser', 'pos': (button_margin + 7 * (button_width + button_margin), button_margin)},
        {'label': 'Size 1', 'pos': (button_margin, button_margin + button_height + button_margin)},
        {'label': 'Size 2', 'pos': (button_margin + button_width + button_margin, button_margin + button_height + button_margin)},
        {'label': 'Size 3', 'pos': (button_margin + 2 * (button_width + button_margin), button_margin + button_height + button_margin)},
        {'label': 'Size 4', 'pos': (button_margin + 3 * (button_width + button_margin), button_margin + button_height + button_margin)},
        {'label': 'Size 5', 'pos': (button_margin + 4 * (button_width + button_margin), button_margin + button_height + button_margin)},
        {'label': 'Brush', 'pos': (button_margin + 5 * (button_width + button_margin), button_margin + button_height + button_margin)},
        {'label': 'Pen', 'pos': (button_margin + 6 * (button_width + button_margin), button_margin + button_height + button_margin)},
        {'label': 'Rectangle', 'pos': (button_margin + 7 * (button_width + button_margin), button_margin + button_height + button_margin)},
        {'label': 'Line', 'pos': (button_margin + 8 * (button_width + button_margin), button_margin + button_height + button_margin)},
        {'label': 'Circle', 'pos': (button_margin + 9 * (button_width + button_margin), button_margin + button_height + button_margin)},
    ]

    # Function to draw on the canvas
    def draw(event, x, y, flags, param):
        nonlocal drawing, brush_size, pen_size, color, shape, x1, y1, line_start

        if event == cv2.EVENT_LBUTTONDOWN:
            if y < button_height * 2 + button_margin * 2:  # Check if click is within button area
                for button in buttons:
                    bx, by = button['pos']
                    if bx <= x <= bx + button_width and by <= y <= by + button_height:
                        handle_action(button['label'].lower())
                        return
            else:
                drawing = True
                x1, y1 = x, y
                if shape == "line":
                    line_start = (x, y)  # Record the starting point for the line

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                if shape == "brush":
                    # Draw a brush stroke on the canvas
                    cv2.circle(canvas, (x, y), brush_size, color, -1)
                elif shape == "pen":
                    # Draw pen stroke on the canvas
                    cv2.circle(canvas, (x, y), pen_size, color, -1)
                elif shape in ["rectangle", "circle"]:
                    # Clear the canvas for shape preview
                    temp_canvas = canvas.copy()
                    if shape == "rectangle":
                        cv2.rectangle(temp_canvas, (x1, y1), (x, y), color, 1)
                    elif shape == "circle":
                        radius = int(((x - x1) ** 2 + (y - y1) ** 2) ** 0.5)
                        cv2.circle(temp_canvas, (x1, y1), radius, color, 1)
                    cv2.imshow('Paint', temp_canvas)
                elif shape == "line" and line_start:
                    # Draw temporary line preview
                    temp_canvas = canvas.copy()
                    cv2.line(temp_canvas, line_start, (x, y), color, 1)
                    cv2.imshow('Paint', temp_canvas)

        elif event == cv2.EVENT_LBUTTONUP:
            if drawing:
                if shape == "brush":
                    # Ensure brush stroke remains on canvas
                    cv2.circle(canvas, (x, y), brush_size, color, -1)
                elif shape == "pen":
                    # Ensure pen stroke remains on canvas
                    cv2.circle(canvas, (x, y), pen_size, color, -1)
                elif shape == "circle":
                    radius = int(((x - x1) ** 2 + (y - y1) ** 2) ** 0.5)
                    cv2.circle(canvas, (x1, y1), radius, color, 1)  # Draw only the outline of the circle
                elif shape == "rectangle":
                    cv2.rectangle(canvas, (x1, y1), (x, y), color, 1)
                elif shape == "line" and line_start:
                    cv2.line(canvas, line_start, (x, y), color, 1)
                drawing = False
                line_start = None

    # Function to handle button actions
    def handle_action(action):
        nonlocal color, brush_size, pen_size, shape
        if action == 'clear':
            canvas[:] = 255
            shape = None
        elif action == 'black':
            color = colors['black']
        elif action == 'red':
            color = colors['red']
        elif action == 'green':
            color = colors['green']
        elif action == 'blue':
            color = colors['blue']
        elif action == 'yellow':
            color = colors['yellow']
        elif action == 'eraser':
            color = colors['white']
        elif action.startswith('size'):
            brush_size = int(action.split()[1])
        elif action == 'brush':
            shape = "brush"
        elif action == 'pen':
            shape = "pen"
        elif action == 'rectangle':
            shape = "rectangle"
        elif action == 'line':
            shape = "line"
        elif action == 'circle':
            shape = "circle"

    # Function to display buttons on the canvas
    def display_buttons(canvas):
        for button in buttons:
            x, y = button['pos']
            draw_stylish_button(canvas, x, y, button_width, button_height, button_radius, button['label'])

    # Bind the draw function to mouse events
    cv2.setMouseCallback('Paint', draw)

    # Main loop for paint editor
    while True:
        display_canvas = canvas.copy()
        display_buttons(display_canvas)
        cv2.imshow('Paint', display_canvas)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC key to exit
            break

    cv2.destroyAllWindows()

# Start the program by showing the landing page
show_landing_page()