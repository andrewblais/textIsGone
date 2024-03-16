from matplotlib.colors import rgb2hex
import numpy as np
from PIL import Image as PILImage
from PIL import ImageTk
from tkinter import *
from tkinter import messagebox


# Define a class for the "Text is Gone" application.
class TextIsGone:
    def __init__(self, root):
        """
        Initialize the application, setting up GUI dimensions, bindings, and widgets.

        :param root: The main window of the application.
        :type root: Tk
        """
        # Application window and size configurations.
        self.root = root
        self.gui_width = 650
        self.gui_height = 625
        # Track the current row for widget placement.
        self.current_row = 0

        # Initialize variables for GUI components and countdown functionality.
        self.title_image = None
        self.gui_typing = None
        self.gui_exit = None
        self.sec_primary = 15  # Initial countdown time in seconds.
        self.sec = self.sec_primary
        self.alpha_val_map = {}  # Maps time to alpha values for text fade effect.

        self.counting_down = True  # Controls the countdown state.

        # Widgets placeholder initialization.
        self.title_image_widg = None
        self.start_button_widg = None
        self.type_text_widg = None
        self.help_button_widg = None
        self.about_button_widg = None
        self.exit_button_widg = None

        # Bind the keyboard event to reset the countdown timer whenever a key is pressed.
        self.root.bind('<Key>', lambda e: self.reset_countdown())

        # Text content for About and Help dialogs.
        self.about_text = """Text is Gone v.1.0\n
        ©2024, MIT License\n
        Andrew Blais\n
        https://github.com/andrewblais"""

        self.help_text = f"""\
        Click Start.\n
        Commence typing.\n
        Copy/Paste your text at any time, but beware:\n
        If 15 seconds goes by without any typing
        your text will disappear forever!\n
        Click Start to go again.\n
        Keep moving and have fun.\n"""

        # Initialize application components.
        self.create_alpha_val_map()  # Create alpha value mapping for text fade effect.
        self.get_title_image()  # Load the title image.
        self.setup_gui()  # Configure GUI elements.

    def get_title_image(self):
        """
        Loads the title image from a predefined path and sets it up for display in the GUI.
        """
        # Load the image and convert it for Tkinter compatibility.
        pil_image = PILImage.open('static/text_is_gone_24.png')
        image_tk_photo_image = ImageTk.PhotoImage(pil_image)
        self.title_image = image_tk_photo_image

    def create_alpha_val_map(self):
        """
        Creates a mapping of seconds to alpha values for fading the text color over time.
        """
        # Generate linearly spaced alpha values and map them to countdown seconds.
        alpha_lin = np.linspace(0, 1, self.sec)
        alpha_enum = enumerate(alpha_lin)
        alpha_dict = {self.sec - i: rgb2hex((a, a, a)) for i, a in alpha_enum}  # noqa
        self.alpha_val_map = alpha_dict

    def increment_row(self):
        """
        Increments the current GUI row, for use in widget placement.
        """
        self.current_row += 1

    def color_fader(self):
        """
        Updates the foreground color of the typing area to fade text based on the remaining seconds.
        """
        # Adjust the text color based on the current second's mapped alpha value.
        self.type_text_widg.configure(fg=self.alpha_val_map[self.sec])

    def help_popup(self):
        """
        Displays a help dialog with instructions on how to use the application.
        """
        messagebox.showinfo("Text is Gone Help", self.help_text, icon="question")

    def about_popup(self):
        """
        Displays an about dialog showing application and author information.
        """
        messagebox.showinfo("About Text is Gone", self.about_text, icon="info")

    def reset_countdown(self):
        """
        Resets the countdown timer to its initial value upon any keyboard activity.
        """
        # Reset the countdown and allow text input again.
        self.sec = self.sec_primary
        self.counting_down = True

    def initiate_countdown(self):
        """
        Initiates the countdown process, enabling text input and starting the fading effect.
        """
        if self.counting_down:
            self.counting_down = False
            self.type_text_widg['state'] = 'normal'
            self.continue_countdown()

    def continue_countdown(self):
        """
        Continues the countdown, updating the text color and, if time expires, clears the text and disables input.
        """
        if self.sec > 0:
            # Continue the countdown, updating text color and decrementing the second counter.
            self.color_fader()
            self.root.after(1000, self.continue_countdown)
            self.sec -= 1
            self.type_text_widg['state'] = 'normal'
            self.start_button_widg['state'] = 'disable'
        else:
            # Once the countdown reaches 0, clear the text area and disable text input.
            self.type_text_widg.delete("1.0", 'end')
            self.type_text_widg['state'] = 'disable'
            self.type_text_widg.configure(fg='#000000')
            self.start_button_widg['state'] = 'normal'

    def setup_gui(self):
        """
        Configures the initial GUI layout, including window size, title, icon, and all interactive widgets.
        """
        # Window configuration and layout setup.
        self.root.title("Text is Gone")
        self.root.iconbitmap('static/icon_32.ico')
        self.root.geometry(f'{self.gui_width}x{self.gui_height}+450+200')
        self.root.minsize(self.gui_width, self.gui_height)
        self.root.maxsize(self.gui_width, self.gui_height)
        self.root.config(padx=60, pady=15)
        for i in range(3):
            self.root.columnconfigure(i, weight=1)

        # Setup and placement of GUI widgets (buttons, text area, labels).
        self.title_image_widg = Label(self.root,
                                      image=self.title_image)
        self.title_image_widg.grid(row=self.current_row,
                                   column=0,
                                   columnspan=3,
                                   pady=(25, 0))

        self.increment_row()

        self.start_button_widg = Button(self.root,
                                        text="START",
                                        cursor='exchange',
                                        font=('Source Sans 3 Black', 12),
                                        width=8,
                                        height=1,
                                        command=self.initiate_countdown)
        self.start_button_widg.grid(row=self.current_row,
                                    column=0,
                                    columnspan=3,
                                    padx=(0, 0),
                                    pady=(35, 0))

        self.increment_row()

        self.type_text_widg = Text(self.root,
                                   width=60,
                                   height=15,
                                   font=('Times New Roman', 12),
                                   wrap=WORD,
                                   padx="15",
                                   pady="10")
        self.type_text_widg.grid(row=self.current_row,
                                 column=0,
                                 columnspan=3,
                                 pady=(35, 0))
        self.type_text_widg['state'] = 'disable'
        self.type_text_widg.focus_set()

        self.increment_row()

        self.help_button_widg = Button(self.root,
                                       text="Help",
                                       cursor="question_arrow",
                                       width=8,
                                       height=1,
                                       command=self.help_popup)
        self.help_button_widg.grid(row=self.current_row,
                                   column=0,
                                   padx=(0, 0),
                                   pady=(60, 0))

        self.about_button_widg = Button(self.root,
                                        text="About",
                                        width=8,
                                        height=1,
                                        command=self.about_popup)
        self.about_button_widg.grid(row=self.current_row,
                                    column=1,
                                    padx=(0, 0),
                                    pady=(60, 0))

        self.exit_button_widg = Button(self.root,
                                       text="Exit",
                                       cursor='trek',
                                       width=8,
                                       height=1,
                                       command=self.root.quit)
        self.exit_button_widg.grid(row=self.current_row,
                                   column=2,
                                   padx=(0, 25),
                                   pady=(60, 0))


if __name__ == '__main__':
    window = Tk()
    text_is_gone = TextIsGone(window)
    window.mainloop()
