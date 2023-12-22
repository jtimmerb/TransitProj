from nyct_gtfs import NYCTFeed

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
        self.train = "F"
        self.station = "F18N"
        self.train_groups = []
        for train_list, api in zip(TRAINS, APIS):
            self.train_groups.append(TrainGroup(train_list, api))

    def get_feed(self):
        for group in self.train_groups:
            if self.train in group.trains:
                feed = NYCTFeed(group.api, api_key=self.api_key)
                return feed.filter_trips(line_id=self.train)
