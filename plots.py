from csv_repository import CalculationWrapper
import matplotlib.pyplot as plt


def plot_deviation_per_sensor(wrapper: CalculationWrapper,
                              show_avg_in_plot=False,
                              show_avg_under_plot=False,
                              show_variation_under_plot=False):
    plt.figure(figsize=(10, 6))

    all_divs = []
    all_expected = []
    all_variations = [69, 69, 69]
    for sensor in wrapper.sensors:
        sensor_divs = [div for div in sensor.additional_payload.get("deviations")]
        all_divs.append(sensor_divs)
        all_expected.append(sensor.additional_payload.get("expected_div"))

    for i, (divs, expected) in enumerate(zip(all_divs, all_expected)):
        plt.plot(divs, label=f"Sensor {i + 1}")
        if (show_avg_in_plot):
            plt.axhline(y=expected, color=f'C{i}', linestyle='--')
            plt.text(0, expected, f'Avg Sensor {i + 1} = {expected}', color=f'C{i}', va='center', ha='left')

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
            [f"AVG Sensor {i + 1}: {avg} metres\n" for i, avg in enumerate(all_expected)])
        plt.figtext(0.05, 0.01, variations_text, fontsize=11, va="bottom", ha="left")

    if show_variation_under_plot and not show_avg_under_plot:
        variations_text = '\n'.join(
            [f"Variation Sensor {i + 1}: +- {variation} metres\n" for i, variation in enumerate(all_variations)])
        plt.figtext(0.05, 0.01, variations_text, fontsize=11, va="bottom", ha="left")
    elif show_variation_under_plot:
        variations_text = '\n'.join(
            [f"Variation Sensor {i + 1}: +- {variation} metres\n" for i, variation in enumerate(all_variations)])
        plt.figtext(0.95, 0.01, variations_text, fontsize=11, va="bottom", ha="right")
    plt.show()
