from csv_repository import CalculationWrapper
import matplotlib.pyplot as plt


def plot_deviation_per_sensor(wrapper: CalculationWrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=False,
                              show_variation_under_plot=False,
                              round_to=4,
                              save_to=None):
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
    plt.title(f'Sensor Abweichungen für Route "{wrapper.route_name}"')
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
