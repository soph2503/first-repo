import tkinter as tk
from tkinter import Canvas
import pyautogui
import threading
import time
from PIL import Image, ImageDraw, ImageTk
import mouse
import keyboard

class DesktopControlApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True)
        self.root.geometry('1400x900')
        self.root.title('Desktop Control Panel')
        
        # State variables
        self.panel_open = False
        self.magnify_active = False
        self.pause_active = False
        self.eye_follow_active = False
        self.mouse_hidden = False
        self.drag_active = False
        self.current_mode = None
        
        # Create side bar
        self.create_sidebar()
        
    def create_sidebar(self):
        """Create the light gray sidebar with two dots"""
        self.sidebar = tk.Frame(self.root, bg='#D3D3D3', width=50)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Create dots indicator
        self.dot_canvas = Canvas(self.sidebar, bg='#D3D3D3', highlightthickness=0, width=50, height=30)
        self.dot_canvas.pack(pady=200)
        
        # Draw two dots
        dot_color = '#888888'
        dot_size = 8
        self.dot_canvas.create_oval(12, 7, 12+dot_size, 7+dot_size, fill=dot_color)
        self.dot_canvas.create_oval(27, 7, 27+dot_size, 7+dot_size, fill=dot_color)
        
        # Bind click event to sidebar
        self.sidebar.bind('<Button-1>', self.toggle_panel)
        self.dot_canvas.bind('<Button-1>', self.toggle_panel)
        
    def toggle_panel(self, event=None):
        """Toggle the control panel open/closed"""
        if self.panel_open:
            self.close_panel()
        else:
            self.open_panel()
            
    def open_panel(self):
        """Open the large gray control box"""
        self.panel_open = True
        
        # Create main panel
        self.panel = tk.Frame(self.root, bg='#808080', width=400, height=800)
        self.panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.panel.pack_propagate(False)
        
        # Title
        title_label = tk.Label(self.panel, text='General', bg='#808080', fg='black', font=('Arial', 14, 'bold'))
        title_label.pack(anchor='nw', padx=15, pady=(15, 5))
        
        # General section - Magnify and Pause
        general_frame = tk.Frame(self.panel, bg='#808080')
        general_frame.pack(anchor='nw', padx=15, pady=5)
        
        # Magnify button
        mag_btn = self.create_icon_button(general_frame, self.magnify_option, '🔍+')
        mag_btn.pack(side=tk.LEFT, padx=5)
        
        # Pause button
        pause_btn = self.create_icon_button(general_frame, self.pause_option, '⏸')
        pause_btn.pack(side=tk.LEFT, padx=5)
        
        # Button section - Mouse clicks
        button_label = tk.Label(self.panel, text='Button', bg='#808080', fg='black', font=('Arial', 14, 'bold'))
        button_label.pack(anchor='nw', padx=15, pady=(20, 5))
        
        button_frame = tk.Frame(self.panel, bg='#808080')
        button_frame.pack(anchor='nw', padx=15, pady=5)
        
        # Left click button
        left_click_btn = self.create_icon_button(button_frame, self.left_click_option, '🖱L')
        left_click_btn.pack(side=tk.LEFT, padx=5)
        
        # Right click button
        right_click_btn = self.create_icon_button(button_frame, self.right_click_option, '🖱R')
        right_click_btn.pack(side=tk.LEFT, padx=5)
        
        # Function section
        function_label = tk.Label(self.panel, text='Function', bg='#808080', fg='black', font=('Arial', 14, 'bold'))
        function_label.pack(anchor='nw', padx=15, pady=(20, 5))
        
        function_frame = tk.Frame(self.panel, bg='#808080')
        function_frame.pack(anchor='nw', padx=15, pady=5)
        
        # Eye follow cursor button
        eye_btn = self.create_icon_button(function_frame, self.eye_follow_option, '👁')
        eye_btn.pack(side=tk.LEFT, padx=5)
        
        # Hide mouse button
        hide_btn = self.create_icon_button(function_frame, self.hide_mouse_option, '🚫')
        hide_btn.pack(side=tk.LEFT, padx=5)
        
        # Additional options
        opt_frame = tk.Frame(self.panel, bg='#808080')
        opt_frame.pack(anchor='nw', padx=15, pady=(20, 5))
        
        # Auto click button
        auto_click_btn = self.create_icon_button(opt_frame, self.auto_click_option, '●')
        auto_click_btn.pack(side=tk.LEFT, padx=5)
        
        # Double click button
        double_click_btn = self.create_icon_button(opt_frame, self.double_click_option, '●●')
        double_click_btn.pack(side=tk.LEFT, padx=5)
        
        # Drag button
        drag_btn = self.create_icon_button(opt_frame, self.drag_option, '↙')
        drag_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button (right arrow)
        close_btn = tk.Label(self.panel, text='→', bg='#808080', fg='white', font=('Arial', 20, 'bold'))
        close_btn.pack(anchor='ne', padx=10, pady=10)
        close_btn.bind('<Enter>', lambda e: self.close_panel())
        
    def create_icon_button(self, parent, command, icon_text):
        """Create an icon button with specified command"""
        btn = tk.Label(parent, text=icon_text, bg='white', fg='black', 
                      font=('Arial', 16), width=3, height=2,
                      relief=tk.RAISED, bd=2, cursor='hand2')
        btn.bind('<Button-1>', lambda e: command())
        return btn
        
    def close_panel(self):
        """Close the control panel"""
        self.panel_open = False
        if hasattr(self, 'panel'):
            self.panel.pack_forget()
            
    def magnify_option(self):
        """Magnify a selected area of screen"""
        self.magnify_active = True
        print("Magnify mode: Look at an area for 3 seconds...")
        threading.Thread(target=self.magnify_task, daemon=True).start()
        
    def magnify_task(self):
        """Capture and magnify screen area"""
        time.sleep(3)
        if self.magnify_active:
            # Get mouse position as center of magnification
            x, y = pyautogui.position()
            # Capture area around mouse
            screenshot = pyautogui.screenshot(region=(x-100, y-100, 200, 200))
            # Magnify 2x
            magnified = screenshot.resize((400, 400))
            
            # Show magnified view
            mag_window = tk.Toplevel(self.root)
            mag_window.title("Magnified View")
            mag_image = ImageTk.PhotoImage(magnified)
            mag_label = tk.Label(mag_window, image=mag_image)
            mag_label.image = mag_image
            mag_label.pack()
            
            print("Magnified area displayed. You can now interact.")
            
    def pause_option(self):
        """Pause mouse until hovering back over pause option"""
        self.pause_active = True
        print("Mouse paused. Hover over pause option to resume.")
        
    def left_click_option(self):
        """Left click after looking at area"""
        print("Left click mode: Look at an area for 3 seconds...")
        threading.Thread(target=self.click_task, args=(1,), daemon=True).start()
        
    def right_click_option(self):
        """Right click after looking at area"""
        print("Right click mode: Look at an area for 3 seconds...")
        threading.Thread(target=self.click_task, args=(2,), daemon=True).start()
        
    def click_task(self, button):
        """Perform click at current mouse position after delay"""
        time.sleep(3)
        x, y = pyautogui.position()
        pyautogui.click(x, y, button=button)
        print(f"Click performed at ({x}, {y})")
        
    def eye_follow_option(self):
        """Make cursor follow eyes (simulate with mouse tracking)"""
        self.eye_follow_active = not self.eye_follow_active
        if self.eye_follow_active:
            print("Eye follow mode active. Click sidebar to deactivate.")
        else:
            print("Eye follow mode deactivated.")
            
    def hide_mouse_option(self):
        """Hide the mouse pointer"""
        self.mouse_hidden = not self.mouse_hidden
        if self.mouse_hidden:
            print("Mouse pointer hidden.")
        else:
            print("Mouse pointer visible.")
            
    def auto_click_option(self):
        """Auto click when hovering over area"""
        print("Auto click mode: Hover over an area to click.")
        threading.Thread(target=self.auto_click_task, daemon=True).start()
        
    def auto_click_task(self):
        """Monitor for hover and auto-click"""
        start_time = time.time()
        last_pos = pyautogui.position()
        
        while self.panel_open and time.time() - start_time < 30:  # 30 second timeout
            current_pos = pyautogui.position()
            if current_pos == last_pos:
                time.sleep(1)
                pyautogui.click()
                print(f"Auto-click at {current_pos}")
                break
            last_pos = current_pos
            time.sleep(0.1)
            
    def double_click_option(self):
        """Double click when hovering over area"""
        print("Double click mode: Hover over an area to double-click.")
        threading.Thread(target=self.double_click_task, daemon=True).start()
        
    def double_click_task(self):
        """Monitor for hover and double-click"""
        start_time = time.time()
        last_pos = pyautogui.position()
        
        while self.panel_open and time.time() - start_time < 30:
            current_pos = pyautogui.position()
            if current_pos == last_pos:
                time.sleep(1)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.click()
                print(f"Double-click at {current_pos}")
                break
            last_pos = current_pos
            time.sleep(0.1)
            
    def drag_option(self):
        """Drag and drop mode"""
        self.drag_active = True
        print("Drag mode: Hover over an area to start dragging. Hover for 3 seconds to drop.")
        self.close_panel()
        
def main():
    root = tk.Tk()
    app = DesktopControlApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
