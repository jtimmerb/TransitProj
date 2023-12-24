import drivers

class LCD_Controller:
    def __init__(self):
        # Load the driver and set it to "display"
        # If you use something from the driver library use the "display." prefix first
        self.display = drivers.Lcd()
    
    def write_to_disp(self, msg, line):
        # Write line of text to the specified line of the display
        # 1 - top line
        # 2 - bottom line
        # print(f"print to line {line}")
        try:
            self.display.lcd_display_string(msg, line)
        except KeyboardInterrupt:
            self.clear_display()

    def clear_display(self):
        # clear LCD
        # print("clearing display")
        self.display.lcd_clear()