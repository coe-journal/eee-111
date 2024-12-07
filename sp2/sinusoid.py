# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: MPL-2.0

from dataclasses import astuple, dataclass
import math

import matplotlib.pyplot as plot



@dataclass
class Arguments:
	@classmethod
	def from_str(cls, frequency: str, duration: str, points: str, show: str) -> "Arguments":
		return Arguments(float(frequency), float(duration), int(points), show == "show")

	def __iter__(self):
		return iter(astuple(self))

	frequency: float
	duration: float
	points: int
	show: bool



def input_list(prompt: str) -> list[str]:
	return [s for s in input(prompt).split()]

def input_arguments(prompt: str) -> Arguments:
	while split := input_list(prompt):
		if len(split) == 3:
			split.append("")

		if len(split) >= 4:
			try:
				return Arguments.from_str(*split[:4])
			except:
				print("Invalid arguments.")
				continue

		print("Invalid number of arguments.")

	assert False, "unreachable"



def range_points(start: float, end: float, points: int) -> list[float]:
	out: list[float] = []
	step = (end - start) / (points - 1)

	current = start
	while current < end:
		out.append(current)
		current += step
	out.append(current)

	return out



def sine_wave(amplitude: float, frequency: float, timepoints: list[float]) -> list[float]:
	return [amplitude * math.sin(2 * math.pi * frequency * timepoint) for timepoint in timepoints]



def plot_data(data: dict[float, float], xlabel: str, ylabel: str) -> None:
	figure, axis = plot.subplots()
	axis.plot(list(data.keys()), list(data.values()))
	plot.xlabel(xlabel)
	plot.ylabel(ylabel)
	plot.show()



def __main__():
	frequency, duration, points, show = input_arguments("> ")

	time = range_points(0, duration, points)
	voltage = sine_wave(1, frequency, time)

	for t, v in zip(time, voltage):
		print(f"{t:.6f} {v:.6f}")

	if show:
		plot_data(dict(zip(time, voltage)), "Time (s)", "Voltage (V)")



__main__()
