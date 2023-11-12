from cmath import sqrt

from csv_repository import DataSeries, SensorData, Measure, CalculationWrapper, Coordinate


def difference_betw_coord(c1: Coordinate, c2: Coordinate):
    difference_coord = Coordinate(long=pow(c1.long - c2.long, 2), lat=pow(c1.lat - c2.lat, 2))
    return sqrt(difference_coord.lat + difference_coord.long)


def calculate_deviations_per_sensor(wrapper: CalculationWrapper):
    for sensor in wrapper.sensors:
        deviations = []
        for i in range(len(sensor.readings)):
            c1 = sensor.readings[i]
            c2 = wrapper.ground_truth[i]
            deviations.append(difference_betw_coord(c1, c2))
        sensor.additional_payload.update({"deviations": deviations})

