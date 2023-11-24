from cmath import sqrt, sin, cos
from math import radians, atan2
from numbers import Complex

from csv_repository import DataSeries, SensorData, Measure, CalculationWrapper, Coordinate


def difference_betw_coord(c1: Coordinate, c2: Coordinate):
    print("coords: " + str(c1) + str(c2))
    difference_coord = Coordinate(long=pow(c1.long - c2.long, 2), lat=pow(c1.lat - c2.lat, 2))
    num: Complex = sqrt(difference_coord.lat + difference_coord.long)
    return num.real


def difference_betw_coord_in_metres(c1: Coordinate, c2: Coordinate) -> float:
    earth_radius = 6371000  # in meters

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = radians(c1.lat), radians(c1.long)
    lat2, lon2 = radians(c2.lat), radians(c2.long)

    # Haversine Formel
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a).real, sqrt(1 - a).real)

    # Calculate distance
    distance = earth_radius * c
    return distance


def calculate_deviations_per_sensor(wrapper: CalculationWrapper):
    for sensor in wrapper.sensors:
        deviations = []
        for i in range(len(sensor.readings)):
            c1 = sensor.readings[i]
            c2 = wrapper.ground_truth[i]
            div = difference_betw_coord_in_metres(c1, c2)
            # print(div)
            deviations.append(div)

        sensor.additional_payload.update({"deviations": deviations})


def calculate_sensor_div_expectation(wrapper: CalculationWrapper):
    for sensor in wrapper.sensors:
        count = 0
        sum = 0
        for div in sensor.additional_payload.get("deviations"):
            sum += div
            count += 1
        sensor.additional_payload.update({"expected_div": sum / count})


def calculate_sensor_div_variance(wrapper: CalculationWrapper):
    for sensor in wrapper.sensors:
        avg = sensor.additional_payload.get("expected_div")
        count = 0
        sum = 0
        for div in sensor.additional_payload.get("deviations"):
            count += 1
            sum += pow(avg-div, 2)

        sensor.additional_payload.update({"deviance": sum / (count - 1)})


def print_expectation_per_sensor(wrapper: CalculationWrapper):
    for sensor in wrapper.sensors:
        print("Expected deviation for '" + str(sensor.sensor_name) + "': " + str(
            sensor.additional_payload.get("expected_div")))


def print_deviation_per_sensor(wrapper: CalculationWrapper):
    for sensor in wrapper.sensors:
        for div in sensor.additional_payload.get("deviations"):
            print(div)
