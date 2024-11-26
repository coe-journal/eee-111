# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: MPL-2.0

from dataclasses import astuple, dataclass
import math

import matplotlib.pyplot as plot



@dataclass
class Arguments:
	@classmethod
	def from_str(cls, frequency0: str, frequency1: str, duration: str, points: str, show: str, bits: str) -> "Arguments":
		return Arguments(float(frequency0), float(frequency1), float(duration), int(points), show == "show", bitstring_to_bools(bits))

	def __iter__(self):
		return iter(astuple(self))

	frequency0: float
	frequency1: float
	duration: float
	points: int
	show: bool
	bits: list[bool]



def bit_to_bool(bit: str) -> bool:
	if bit == '0':
		return False
	elif bit == '1':
		return True

	raise ValueError("Invalid character.")

def bitstring_to_bools(bits: str) -> list[bool]:
	return [bit_to_bool(b) for b in bits]



def input_list(prompt: str) -> list[str]:
	return [s for s in input(prompt).split()]

def input_arguments(prompt: str) -> Arguments:
	while split := input_list(prompt):
		if len(split) == 4:
			split.append("")

		if len(split) >= 5:
			try:
				split = split[:5]
				split.append(input(prompt))
				return Arguments.from_str(*split)
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
	frequency0, frequency1, duration, points, show, bits = input_arguments("> ")



__main__()
