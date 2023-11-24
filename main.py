from csv_repository import DataSeries, print_sensor_data
from calculations import *
from plots import *


def main():
    data_series: DataSeries = DataSeries.parse_from_csv("demo.csv")
    calculation_wrapper = data_series.extract_calc_wrapper()

    calculate_deviations_per_sensor(calculation_wrapper)
    calculate_sensor_div_expectation(calculation_wrapper)

    plot_deviation_per_sensor(calculation_wrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=True,
                              show_variation_under_plot=True)

    print_expectation_per_sensor(calculation_wrapper)


if __name__ == '__main__':
    main()
