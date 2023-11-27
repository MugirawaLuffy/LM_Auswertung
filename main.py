import os
import sys
import time

from calculations import *
from plots import *
import shutil

def generate_from_path(path, save_to=None):
    data_series: DataSeries = DataSeries.parse_from_csv(path)
    calculation_wrapper = data_series.extract_calc_wrapper()
    interpolate_all_readings(calculation_wrapper)

    calculate_deviations_per_sensor(calculation_wrapper)
    calculate_sensor_div_expectation(calculation_wrapper)
    calculate_sensor_div_variance(calculation_wrapper)



    plot_deviation_per_sensor(calculation_wrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=True,
                              show_variation_under_plot=True,
                              round_to=3,
                              save_to=save_to+calculation_wrapper.route_name+"_both_under.png",
                              interpolation="1s")
    plot_deviation_per_sensor(calculation_wrapper,
                              show_avg_in_plot=True,
                              show_avg_under_plot=True,
                              show_variation_under_plot=True,
                              round_to=3,
                              save_to=save_to+calculation_wrapper.route_name + "avg_in_plot.png",
                              interpolation="1s")
    plot_deviation_per_sensor(calculation_wrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=False,
                              show_variation_under_plot=False,
                              round_to=3,
                              save_to=save_to+calculation_wrapper.route_name + "clean.png",
                              interpolation="1s")

    save_to += "/cdf/" # <- following files should be saved in cdf subdir
    for sensor in calculation_wrapper.sensors:
        plot_cdf_and_confidence(calculation_wrapper.sensors[0], save_to=save_to + sensor.sensor_name + "_default.png")
        plot_cdf_and_confidence(calculation_wrapper.sensors[0], save_to=save_to + sensor.sensor_name + "_clean.png",
                                highlight_50_ci=False,
                                highlight_95_ci=False,
                                show_interval_in_graph=False,
                                interpolation="1s")
        plot_cdf_and_confidence(calculation_wrapper.sensors[0], save_to=save_to + sensor.sensor_name + "_subtle.png",
                                highlight_50_ci=False,
                                highlight_95_ci=False,
                                interpolation="1s")



def main():
    path = "analyse"
    print('Processing ', len(sys.argv), ' files:')
    files = sys.argv[1:]
    print(files)

    if os.path.isdir(path):
        shutil.rmtree(path)

    if not os.path.isdir(path):
        os.makedirs(path)

    counter = 0
    for file in files:
        counter += 1
        if not os.path.isdir(file):
            os.makedirs(path + "/" + file.split(".")[0] + "_" + str(counter) + "/cdf")
            generate_from_path(path=file, save_to=path + "/" + file.split(".")[0] + "_" + str(counter) + "/")


def debug():
    data_series: DataSeries = DataSeries.parse_from_csv("demo.csv")
    calculation_wrapper = data_series.extract_calc_wrapper()
    calculation_wrapper = interpolate_all_readings(calculation_wrapper)

    print(f"Now got {len(calculation_wrapper.sensors[0].readings)} readings")

    calculate_deviations_per_sensor(calculation_wrapper)
    calculate_sensor_div_expectation(calculation_wrapper)
    calculate_sensor_div_variance(calculation_wrapper)

    print("plotting")
    plot_deviation_per_sensor(calculation_wrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=True,
                              show_variation_under_plot=True,
                              round_to=3,)


if __name__ == '__main__':
    """
    print(time.time_ns())
    time.sleep(3)
    print(time.time_ns())
    time.sleep(5)
    print(time.time_ns())
    """
    # debug()
    main()
