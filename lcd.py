import drivers

class LCD_Controller:
    def __init__(self):
        # Load the driver and set it to "display"
        # If you use something from the driver library use the "display." prefix first
        self.display = drivers.Lcd()
    
    def write_to_disp(self, msg, line):
        # Write line of text to first line of display
        print("Writing to display")
        self.display.lcd_display_string(msg, line)  

    def clear_display(self):
        print("Cleaning up!")
        self.display.lcd_clear()