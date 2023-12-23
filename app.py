from mtafeedhandler import MTASubwayFeedHandler

import threading
import schedule
import time
from lcd import LCD_Controller

class App:
    def __init__(self):
        self.feed_handler = MTASubwayFeedHandler()
        self.lcd = LCD_Controller()

    def set_train(self, train):
        self.feed_handler.train = train

    def get_train(self):
        return self.feed_handler.train

    def set_station(self, station):
        self.feed_handler.station = station

    def get_station(self):
        return self.feed_handler.station

    def start_update_train(self):
        schedule.every(2).seconds.do(self.update_feed)
        # Start the background thread
        self.stop_run_continuously = self.run_continuously()

    def stop_update(self):
        # Stop the background thread
        self.stop_run_continuously.set()

    def run_continuously(self, interval=1):
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def update_feed(self):
        feed = self.feed_handler.get_feed()
        stops = self.update_station_arrivals(feed)
        for stop, line in zip(stops,[1,2]):
            self.lcd.write_to_disp(f"{self.get_train()} train is expected to arrive at {self.get_station()} at {stop.arrival}", line)

    def update_station_arrivals(self,feed):
        stop_list = []
        for trip in feed:
            for stop in trip.stop_time_updates:
                if stop.stop_id == self.get_station():
                    stop_list.append(stop)
                    break
        if stop_list.__len__() > 2:
            return stop_list[:2]
        return stop_list
    
        ### TODO Check ID of trips to make sure I'm not adding duplicate trips to the update list
