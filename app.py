from nyct_gtfs import NYCTFeed
import threading
import schedule
import time


class TrainGroup:
    def __init__(self, trains, api):
        self.trains = trains
        self.api = api


class MTASubwayFeedHandler:
    def __init__(self):
        API_KEY = "MsGGWvRfMp2sunZAbEHnb7ZkXkIlDCw72fK8KTmc"

        TRAINS = [
            ["A", "C", "E"],
            ["B", "D", "F", "M"],
            ["G"],
            ["J", "Z"],
            ["N", "Q", "R", "W"],
            ["L"],
            ["1", "2", "3", "4", "5", "6", "7", "S"],
        ]

        APIS = [
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
        ]

        self.api_key = API_KEY

        self.train_groups = []
        for train_list, api in zip(TRAINS, APIS):
            self.train_groups.append(TrainGroup(train_list, api))

    def get_feed(self, train):
        for group in self.train_groups:
            if train in group.trains:
                feed = NYCTFeed(group.api, api_key=self.api_key)
                return feed.filter_trips(line_id=train)


class App:
    def __init__(self):
        self.handler = MTASubwayFeedHandler()
        # set a default line to watch
        self.set_train("A")

    def set_train(self, train):
        self.train = train

    def start_update(self):
        schedule.every(2).seconds.do(self.update_train)
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

    def update_train(self):
        feed = self.handler.get_feed(self.train)
        print(feed[0])
