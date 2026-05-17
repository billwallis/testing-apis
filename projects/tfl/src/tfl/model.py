import dataclasses


@dataclasses.dataclass
class JourneyPlannerSearchParams:
    """
    Search parameters for the Journey Planner.

    :param via: Travel through point on the journey. Can be WGS84
        coordinates expressed as "lat,long", a UK postcode, a Naptan
        (StopPoint) id, an ICS StopId, or a free-text string (will cause
        disambiguation unless it exactly matches a point of interest name).
    :param national_search: Does the journey cover stops outside London?
    :param date: The date must be in yyyyMMdd format.
    :param time: The time must be in HHmm format.
    :param time_is: Does the time given relate to arrival or leaving time?
        Possible options: "departing" | "arriving"
    :param journey_preference: The journey preference eg possible options:
        "leastinterchange" | "leasttime" | "leastwalking"
    :param mode: The mode must be a comma separated list of modes. eg
        possible options: "public-bus,overground,train,tube,coach,dlr,cablecar,tram,river,walking,cycle"
    :param accessibility_preference: The accessibility preference must be a
        comma separated list eg. "noSolidStairs,noEscalators,noElevators,stepFreeToVehicle,stepFreeToPlatform"
    :param from_name: An optional name to associate with the origin of the
        journey in the results.
    :param to_name: An optional name to associate with the destination of the
        journey in the results.
    :param via_name: An optional name to associate with the via point of the
        journey in the results.
    :param max_transfer_minutes: The max walking time in minutes for
        transfer eg. "120"
    :param max_walking_minutes: The max walking time in minutes for journeys
        eg. "120"
    :param walking_speed: The walking speed. eg possible options: "slow" |
        "average" | "fast".
    :param cycle_preference: The cycle preference. eg possible options:
        "allTheWay" | "leaveAtStation" | "takeOnTransport" | "cycleHire"
    :param adjustment: Time adjustment command. eg possible options:
        "TripFirst" | "TripLast"
    :param bike_proficiency: A comma separated list of cycling proficiency
        levels. eg possible options: "easy,moderate,fast"
    :param alternative_cycle: Option to determine whether to return
        alternative cycling journey.
    :param alternative_walking: Option to determine whether to return
        alternative walking journey.
    :param apply_html_markup: Flag to determine whether certain text (e.g.
        walking instructions) should be output with HTML tags or not.
    :param use_multi_modal_call: A boolean to indicate whether or not to
        return 3 public transport journeys, a bus journey, a cycle hire
        journey, a personal cycle journey and a walking journey.
    :param walking_optimization: A boolean to indicate whether to optimize
        journeys using walking.
    :param taxi_only_trip: A boolean to indicate whether to return one or
        more taxi journeys. Note, setting this to true will override
        "useMultiModalCall".
    :param route_between_entrances: A boolean to indicate whether public
        transport routes should include directions between platforms and
        station entrances.
    :param use_real_time_live_arrivals: A boolean to indicate if we want to
        receive real time live arrivals data where available.
    :param calc_one_direction: A boolean to make Journey Planner calculate
        journeys in one temporal direction only. In other words, only
        calculate journeys after the 'depart' time, or before the 'arrive'
        time. By default, the Journey Planner engine (EFA) calculates
        journeys in both temporal directions.
    :param include_alternative_routes: A boolean to make Journey Planner
        return alternative routes. Alternative routes are calculated by
        removing one or more lines included in the fastest route and
        re-calculating. By default, these journeys will not be returned.
    :param override_multi_modal_scenario: Format - int32. An optional
        integer to indicate what multi modal scenario we want to use.
    :param combine_transfer_legs: A boolean to indicate whether walking leg
        to station entrance and walking leg from station entrance to
        platform should be combined. Defaults to true.
    """

    via: str | None = None
    national_search: bool | None = None
    date: str | None = None
    time: str | None = None
    time_is: str | None = None
    journey_preference: str | None = None
    mode: list[str] | None = None
    accessibility_preference: str | None = None
    from_name: str | None = None
    to_name: str | None = None
    via_name: str | None = None
    max_transfer_minutes: str | None = None
    max_walking_minutes: str | None = None
    walking_speed: str | None = None
    cycle_preference: str | None = None
    adjustment: str | None = None
    bike_proficiency: str | None = None
    alternative_cycle: bool | None = None
    alternative_walking: bool | None = None
    apply_html_markup: bool | None = None
    use_multi_modal_call: bool | None = None
    walking_optimization: bool | None = None
    taxi_only_trip: bool | None = None
    route_between_entrances: bool | None = None
    use_real_time_live_arrivals: bool | None = None
    calc_one_direction: bool | None = None
    include_alternative_routes: bool | None = None
    override_multi_modal_scenario: int | None = None
    combine_transfer_legs: bool | None = None

    def to_dict(self) -> dict:
        """
        Convert the dataclass to a dictionary.
        """
        return dataclasses.asdict(self)  # type: ignore

    def to_params(self) -> str:
        """
        Convert the dataclass to a query string.
        """
        return "&".join(
            f"{key}={value}"
            for key, value in self.to_dict().items()
            if value is not None
        )
