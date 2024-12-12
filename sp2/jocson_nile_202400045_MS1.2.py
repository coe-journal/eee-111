# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from dataclasses import dataclass
from functools import partial
from typing import Any, Callable

import math

import matplotlib.pyplot as plot



@dataclass
class Transform:
	convert : type | Callable
	position: int

@dataclass
class Rule:
	transforms : list[Transform]
	find_string: str | None = None

@dataclass
class CommandSpec:
	rules   : list[Rule]
	callback: Callable[..., bool]



def input_list(prompt: str) -> list[str]:
	return input(prompt).split()



def parse_rules(rules: list[Rule], command: list[str]) -> list[Any] | None:
	if len(command) != len(rules):
		return None

	outputs = 0
	for rule in rules:
		outputs += len(rule.transforms)

	parsed: list[Any] = [None] * outputs

	for rule, arg in zip(rules, command):
		if rule.find_string != None and rule.find_string != arg:
			return None

		try:
			for transform in rule.transforms:
				parsed[transform.position] = transform.convert(arg)

		except:
			return None

	return parsed

def try_commandspecs(specs: list[CommandSpec], command: list[str], default: Callable[[], bool]) -> bool:
	for spec in specs:

		if (parsed := parse_rules(spec.rules, command)) != None:
			return spec.callback(*parsed)

	return default()



def arange(start: float, end: float, points: int) -> list[float]:
	r: list[float] = []
	step = (end - start) / (points - 1)

	current = start
	for _ in range(points):
		r.append(current)
		current += step

	return r



def sine(frequency: float, phase_shift: float, t: float) -> float:
	return math.sin(2 * math.pi * frequency * (t - phase_shift))

def time_value(f: Callable[[float], float], start: float, end: float, points: int) -> list[tuple[float, float]]:
	tv: list[tuple[float, float]] = []

	for t in arange(start, end, points):
		tv.append((t, f(t)))

	return tv

def fsk(frequency0: float, frequency1: float, duration: float, points: int, bits: str) -> list[tuple[float, float]]:
	fsk: list[tuple[float, float]] = []

	n = len(bits)

	endpoints = arange(0, duration, n + 1)
	for i in range(n):
		start = endpoints[i]
		end = endpoints[i + 1]

		frequency = frequency0
		if bits[i] == "1":
			frequency = frequency1

		fsk.extend(time_value(partial(sine, frequency, (end - start) * i), start, end, points // n + 1))
		fsk.pop()

	fsk.append((duration, 0))

	return fsk



def bitstring(s: str) -> str:
	if all(c in '01' for c in s):
		return s

	else:
		raise ValueError("The given string is not a bitstring.")



def print_fsk(freq0: float, freq1: float, dur: float, pts: int) -> bool:
	if parsed := parse_rules(
		[Rule([Transform(bitstring, 0)])],
		input_list("> ")
	):
		bits = parsed[0]
		tv = fsk(freq0, freq1, dur, pts, bits)
		for t, v in tv:
			print(f"{t:.9f} {v:.9f}")

	return True

def plot_fsk(freq0: float, freq1: float, dur: float, pts: int) -> bool:
	if parsed := parse_rules(
		[Rule([Transform(bitstring, 0)])],
		input_list("> ")
	):
		bits = parsed[0]
		tv = fsk(freq0, freq1, dur, pts, bits)
		figure, axis = plot.subplots()
		axis.plot(*zip(*tv))
		plot.show()

	return True

def out_fsk(freq0: float, freq1: float, dur: float, pts: int, filename: str) -> bool:
	if parsed := parse_rules(
		[Rule([Transform(bitstring, 0)])],
		input_list("> ")
	):
		bits = parsed[0]
		tv = fsk(freq0, freq1, dur, pts, bits)
		with open(filename, "w") as file:
			for t, v in tv:
				print(f"{t:.9f} {v:.9f}", file=file)

	return True



def help_string(info: str | None = None) -> bool:
	if info != None:
		info += "\n"

	else:
		info = ""

	print(f"""{ info }Usage:
	<freq0:float> <freq1:float> <dur:float> <pts:int>                    Generates the time-voltage format of a FSK signal.
	<bits:str>
	<freq0:float> <freq1:float> <dur:float> <pts:int> plot               Same as the first, but shows a plot of the signal.
	<bits:str>
	<freq0:float> <freq1:float> <dur:float> <pts:int> out <filename:str> Same as the first, but saves the values into a file.
	<bits:str>
	help                                                                 Prints this message.
	exit                                                                 Exits the program."""
	)

	return True



def run_command(command: list[str]) -> bool:
	return try_commandspecs(
		[
			CommandSpec(
				[
					Rule([Transform(float, 0)]),
					Rule([Transform(float, 1)]),
					Rule([Transform(float, 2)]),
					Rule([Transform(int, 3)])
				],
				print_fsk
			),

			CommandSpec(
				[
					Rule([Transform(float, 0)]),
					Rule([Transform(float, 1)]),
					Rule([Transform(float, 2)]),
					Rule([Transform(int, 3)]),
					Rule([], "plot")
				],
				plot_fsk
			),

			CommandSpec(
				[
					Rule([Transform(float, 0)]),
					Rule([Transform(float, 1)]),
					Rule([Transform(float, 2)]),
					Rule([Transform(int, 3)]),
					Rule([], "out"),
					Rule([Transform(str, 4)])
				],
				out_fsk
			),

			CommandSpec(
				[
					Rule([], "help")
				],
				lambda: help_string()
			),

			CommandSpec(
				[
					Rule([], "exit")
				],
				lambda: False
			)
		],
		command,
		lambda: help_string("Invalid arguments provided.")
	)



def __main__():
	while True:
		try:
			if run_command(input_list("> ")) == False:
				return

		except Exception as e:
			print(e)

		print("")



__main__()
