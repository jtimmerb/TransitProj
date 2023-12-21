from app import App
import time

application = App()
application.start_app()

time.sleep(10)
application.stop_update()
