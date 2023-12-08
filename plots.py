import numpy as np
from numpy import arange
from scipy import stats
from csv_repository import CalculationWrapper, SensorData
import matplotlib.pyplot as plt


def plot_deviation_per_sensor(wrapper: CalculationWrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=False,
                              show_variation_under_plot=False,
                              round_to=4,
                              save_to=None,
                              interpolation=None):
    plt.figure(figsize=(10, 6))

    all_divs = []
    all_expected = []
    all_variations = []
    for sensor in wrapper.sensors:
        sensor_divs = [div for div in sensor.additional_payload.get("deviations")]
        all_divs.append(sensor_divs)

        all_expected.append(round(sensor.additional_payload.get("expected_div"), round_to))
        all_variations.append(round(sensor.additional_payload.get("deviance"), round_to))

    for i, (divs, expected) in enumerate(zip(all_divs, all_expected)):
        plt.plot(divs, label=f"Sensor {wrapper.sensors[i].sensor_name}")
        if (show_avg_in_plot):
            plt.axhline(y=expected, color=f'C{i}', linestyle='--')
            plt.text(0, expected, f'Avg dist {wrapper.sensors[i].sensor_name} = {expected}', color=f'C{i}', va='center',
                     ha='left')

    plt.xlabel('Data Points')
    plt.ylabel('Deviation (m)')
    plt.title(f'Sensor Abweichungen für Route "{wrapper.route_name}" (interp: {interpolation})')
    plt.legend()
    plt.grid(True)

    num_data_points = len(all_divs[0])
    plt.xticks(range(num_data_points))

    if show_variation_under_plot or show_avg_under_plot:
        plt.subplots_adjust(bottom=0.3)

    if show_avg_under_plot:
        variations_text = '\n'.join(
            [f"Erwartungswert Distanz ({wrapper.sensors[i].sensor_name}): {avg} metres\n" for i, avg in
             enumerate(all_expected)])
        plt.figtext(0.05, 0.01, variations_text, fontsize=11, va="bottom", ha="left")

    if show_variation_under_plot and not show_avg_under_plot:
        variations_text = '\n'.join(
            [f"Standard Abweichung von {wrapper.sensors[i].sensor_name}: +- {variation} metres\n" for i, variation in
             enumerate(all_variations)])
        plt.figtext(0.05, 0.01, variations_text, fontsize=11, va="bottom", ha="left")
    elif show_variation_under_plot:
        variations_text = '\n'.join(
            [f"Standard Abweichung: +- {variation} metres\n" for i, variation in enumerate(all_variations)])
        plt.figtext(0.95, 0.01, variations_text, fontsize=11, va="bottom", ha="right")



    if save_to is not None:
        plt.savefig(save_to)
    else:
        plt.show()


def plot_cdf_and_confidence(data: SensorData,
                            show_interval_in_graph=True,
                            show_interval_underneath=True,
                            highlight_50_ci=True,
                            highlight_95_ci=True,
                            round_to=4,
                            save_to=None,
                            interpolation=None):
    # Extract relevant data
    deviations = data.additional_payload.get("deviations", [])
    expected_div = data.additional_payload.get("expected_div", 0)
    deviance = data.additional_payload.get("deviance", 0)

    # Plot the cumulative distribution function (CDF) of positioning error
    x = np.sort(deviations)
    y = np.arange(1, len(x) + 1) / len(x)

    # Plot the CDF
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title(f'CDF von {data.sensor_name}')
    plt.xlabel(f'Positionierungsfehler (interpolation: {interpolation})')
    plt.ylabel('Kumulative Wkt.')
    plt.grid(True)

    # Calculate positioning error with 50% and 95% confidence intervals based on the deviation from the expected_div
    conf_interval_50 = list(stats.norm.interval(0.50, loc=expected_div, scale=deviance))
    conf_interval_95 = list(stats.norm.interval(0.95, loc=expected_div, scale=deviance))

    conf_interval_50[0] = round(conf_interval_50[0], round_to)
    conf_interval_50[1] = round(conf_interval_50[1], round_to)
    conf_interval_95[0] = round(conf_interval_95[0], round_to)
    conf_interval_95[1] = round(conf_interval_95[1], round_to)

    # print(f"Positioning Error with 50% confidence interval: {conf_interval_50}")
    # print(f"Positioning Error with 95% confidence interval: {conf_interval_95}")

    if show_interval_underneath:
        plt.subplots_adjust(bottom=0.2)
        confidences = (f"50% Konfidenzinterval: {conf_interval_50}\n"
                       f"95% Konfidenzinterval: {conf_interval_95}")
        plt.figtext(0.05, 0.01, confidences, fontsize=11, va="bottom", ha="left")

    if show_interval_in_graph:
        plt.axvline(x=conf_interval_50[0], color='y', linestyle='--', label='50% CI Lower')
        plt.axvline(x=conf_interval_50[1], color='y', linestyle='--', label='50% CI Upper')
        plt.axvline(x=conf_interval_95[0], color='r', linestyle='--', label='95% CI Lower')
        plt.axvline(x=conf_interval_95[1], color='r', linestyle='--', label='95% CI Upper')

        if highlight_95_ci:
            plt.axvspan(conf_interval_95[0], conf_interval_95[1], color='r', alpha=0.3)

        if highlight_50_ci:
            plt.axvspan(conf_interval_50[0], conf_interval_50[1], color='y', alpha=0.3)

    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    plt.draw()
    plt.show()

    if save_to is not None:
        plt.savefig(save_to)
    else:
        plt.show()

    plt.close()
