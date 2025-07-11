"""
Manual testing for the API clients.
"""

from src import utils
from src.apis import tfl


def main() -> None:
    """
    Manually test the API client.
    """
    tfl_connector = tfl.TFLConnector()

    utils.pprint(tfl_connector.get_accident_stats(2025).json())
    utils.pprint(tfl_connector.get_air_quality().json())

    utils.pprint(tfl_connector.get_bike_points().json())
    utils.pprint(
        tfl_connector.get_bike_points(bike_point_id="BikePoints_608").json()
    )
    utils.pprint(tfl_connector.get_bike_points(query="Holborn").json())

    # These were returning HTML?!
    print(tfl_connector.get_crowding(naptan="940GZZLUBST").text)
    print(
        tfl_connector.get_crowding(
            naptan="940GZZLUBST", day_of_week="Live"
        ).text
    )
    print(
        tfl_connector.get_crowding(
            naptan="940GZZLUBST", day_of_week="Monday"
        ).text
    )

    utils.pprint(tfl_connector.get_journey().json())
    utils.pprint(tfl_connector.get_journey(meta=True).json())

    journey_params = tfl.JourneyPlannerSearchParams(
        calc_one_direction=True,
        include_alternative_routes=False,
    )
    utils.pprint(
        tfl_connector.get_journey_plan(
            from_="4900000248S",  # London Victoria
            to="490000080A",  # Farringdon Station
            search_params=journey_params,
        ).json()
    )

    utils.pprint(tfl_connector.get_network_status().json())


if __name__ == "__main__":
    main()
