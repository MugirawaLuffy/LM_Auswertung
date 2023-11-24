import os

from csv_repository import DataSeries, print_sensor_data
from calculations import *
from plots import *


def generate_from_path(path, save_to=None):
    data_series: DataSeries = DataSeries.parse_from_csv(path)
    calculation_wrapper = data_series.extract_calc_wrapper()

    calculate_deviations_per_sensor(calculation_wrapper)
    calculate_sensor_div_expectation(calculation_wrapper)
    calculate_sensor_div_variance(calculation_wrapper)

    plot_deviation_per_sensor(calculation_wrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=True,
                              show_variation_under_plot=True,
                              round_to=3,
                              save_to=save_to)

    print_expectation_per_sensor(calculation_wrapper)


def main():
    path = "analyse"
    files = ["demo.csv", "demo2.csv"]

    if not os.path.isdir(path):
        os.makedirs(path)

    for file in files:
        if not os.path.isdir(file):
            os.makedirs(path + "/" + file.split(".")[0])
            generate_from_path(file, "pic.png")


if __name__ == '__main__':
    main()
