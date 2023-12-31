from copy import copy
from dataclasses import dataclass

CSV_ROW_DELIMITER = "\n"
CSV_COL_DELIMITER = ","


def read_file_into_lines(file_name: str):
    to_return: [str] = []
    with open(file_name) as file:
        text = file.read()
        to_return = text.split(CSV_ROW_DELIMITER)

    return to_return


def pairwise(iterable):
    # s -> (s0, s1), (s2, s3), (s4, s5), ...
    a = iter(iterable)
    return zip(a, a)


@dataclass
class Coordinate:
    long: float
    lat: float
    timestamp_nano: int = 0


@dataclass
class Measure:
    ground_truth: Coordinate
    sensor_readings: list[Coordinate]
    timestamp: int = 0

    # CSV has format: GT lon | GT lat | timestamp | s1 long | s1 lat ...
    @staticmethod
    def parse_from_csv_line(line: str):
        cols = line.split(CSV_COL_DELIMITER)
        to_return: Measure = Measure(
            Coordinate(long=float(cols[0]), lat=float(cols[1]), timestamp_nano=int(cols[2])), sensor_readings=[])

        to_return.timestamp = int(cols[2])

        for lon, lat in pairwise(cols[3:]):
            to_return.sensor_readings.append(Coordinate(long=float(lon), lat=float(lat), timestamp_nano=int(cols[2])))

        return to_return

    def __str__(self):
        return str(self.sensor_readings)


@dataclass
class SensorData:
    sensor_name = "unnamed"
    readings: list[Coordinate]
    additional_payload: dict


@dataclass
class CalculationWrapper:
    route_name: str
    ground_truth: list[Coordinate]
    sensors: list[SensorData]


@dataclass
class DataSeries:
    sensor_labels: list[str]
    readings: list[Measure]
    ground_truth_route_name: str = "unnamed"

    def __repr__(self):
        return str(self.readings)

    def __str__(self):
        return str(self.readings)

    @staticmethod
    def parse_from_csv(file_name: str):
        to_return = DataSeries([], [])
        to_return.sensor_labels = []
        to_return.readings = []
        lines = read_file_into_lines(file_name)

        # first line is used for metadata: ---- route name | sensor1 name | sensor2 name | ... sensor n name -----
        metadata = lines[0].split(CSV_COL_DELIMITER)
        to_return.ground_truth_route_name = metadata[0]

        # rest of metadata contains labels
        for label_index in range(1, len(metadata)):
            label = metadata[label_index]
            if label != '':
                to_return.sensor_labels.append(label)

        # rest of lines contains readings ... parse
        for reading_index in range(1, len(lines)):
            line_str = lines[reading_index]
            if line_str != '':
                line: Measure = Measure.parse_from_csv_line(line_str)

            to_return.readings.append(copy(line))

        return to_return

    def extract_sensor_data_positional(self, index):
        sensor_readings = []
        for reading in range(len(self.readings)):
            entry: Coordinate = self.readings[reading].sensor_readings[index]
            sensor_readings.append(entry)

        to_return = SensorData(sensor_readings, {})
        to_return.sensor_name = self.sensor_labels[index]
        return to_return

    def extract_calc_wrapper(self):
        gt = []
        sensors = []
        for sensor_index in range(len(self.sensor_labels)):
            sensors.append(self.extract_sensor_data_positional(sensor_index))

        for reading in range(len(self.readings)):
            gt.append(self.readings[reading].ground_truth)

        return CalculationWrapper(sensors=sensors, ground_truth=gt, route_name=self.ground_truth_route_name)

    def print_series(self):
        for r in self.readings:
            print(r.sensor_readings)


def print_sensor_data(wrapper: CalculationWrapper):
    data = wrapper.sensors
    sensor_names = ""
    for i in range(len(data)):
        sensor_names += data[i].sensor_name
        if i < (len(data) - 1):
            sensor_names += ", "

    print("Got {} sensors ({})".format(len(data), sensor_names))
