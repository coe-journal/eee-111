# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: MPL-2.0

from dataclasses import astuple, dataclass
import math



@dataclass
class Arguments:
	@classmethod
	def from_str(cls, frequency1: str, frequency2: str, duration: str, points: str, bits: str) -> "Arguments":
		return Arguments(float(frequency1), float(frequency2), float(duration), int(points), validate_bitstring(bits))

	def __iter__(self):
		return iter(astuple(self))

	frequency1: float
	frequency2: float
	duration: float
	points: int
	bits: str



def validate_bitstring(bits: str) -> str:
	if all(b in "01" for b in bits):
		return bits

	raise ValueError("Invalid characters in bitstring.")



def input_list(prompt: str) -> list[str]:
	return [s for s in input(prompt).split()]

def input_arguments(prompt: str) -> Arguments:
	while split := input_list(prompt):
		if len(split) >= 4:
			try:
				split = split[:4]
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



def __main__():
	frequency1, frequency2, duration, points, bits = input_arguments("> ")



__main__()
