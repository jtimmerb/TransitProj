from nyct_gtfs import NYCTFeed


class TrainGroup:
    def __init__(self, trains, api):
        self.trains = trains
        self.api = api


class MTASubwayFeedHandler:
    def __init__(self, API_KEY, TRAINS, APIS):
        self.api_key = API_KEY

        self.train_groups = []
        for train_list, api in zip(TRAINS, APIS):
            self.train_groups.append(TrainGroup(train_list, api))

    def get_feed(self, train):
        for group in self.train_groups:
            if train in group.trains:
                return NYCTFeed(group.api, api_key=self.api_key)


def start_application():
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

    return MTASubwayFeedHandler(API_KEY, TRAINS, APIS)


handler = start_application()
feed = handler.get_feed("A")
print(feed.trips[0])
