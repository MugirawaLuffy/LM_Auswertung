from csv_repository import DataSeries, print_sensor_data
from calculations import calculate_deviations_per_sensor


def main():
    data_series = DataSeries.parse_from_csv("demo.csv")
    calculation_wrapper = data_series.extract_calc_wrapper()
    print_sensor_data(calculation_wrapper)
    calculate_deviations_per_sensor(calculation_wrapper)



if __name__ == '__main__':
    main()
