# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: MPL-2.0

from dataclasses import astuple, dataclass

import math



@dataclass
class Arguments:
	@classmethod
	def from_str(cls, frequency: str, duration: str, points: str, show: str) -> "Arguments":
		return Arguments(float(frequency), float(duration), int(points), show == "true")

	def __iter__(self):
		return iter(astuple(self))

	frequency: float
	duration: float
	points: int
	show: bool



def input_list(prompt: str) -> list[str]:
	return [s for s in input(prompt).split()]

def input_arguments(prompt: str) -> Arguments:
	split = input_list(prompt)
	return Arguments.from_str(*split)



def range_points(start: float, end: float, points: int) -> list[float]:
	out: list[float] = []
	step = (end - start) / (points - 1)

	while True:
		out.append(start)
		start += step
		if start > end:
			break

	return out



def sine_wave(amplitude: float, frequency: float, timepoints: list[float]) -> list[float]:
	out: list[float] = []

	for timepoint in timepoints:
		out.append(amplitude * math.sin(2 * math.pi * frequency * timepoint))

	return out



def __main__():
	frequency, duration, points, show = input_arguments("> ")

	time = range_points(0, duration, points)
	voltage = sine_wave(1, frequency, time)

	for t, v in zip(time, voltage):
		print(t, v)



__main__()
