# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from dataclasses import dataclass
from itertools import pairwise
from typing import Any, Callable



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



def print_crossing(pts: int) -> bool:
	tv: list[tuple[float, float]] = []

	for _ in range(pts):
		if parsed := parse_rules(
			[Rule([Transform(float, 0)]), Rule([Transform(float, 1)])],
			input_list("> ")
		):
			t = parsed[0]
			v = parsed[1]

			tv.append((t, v))

	tv = [xy for xy in tv if xy[1] != 0]

	crossings = 0
	for x, y in pairwise(tv):
		if x[1] * y[1] < 0:
			crossings += 1

	print(crossings)

	return True



def help_string(info: str | None = None) -> bool:
	if info != None:
		info += "\n"

	else:
		info = ""

	print(f"""{ info }Usage:
	<pts:int>               Outputs the number of zero-crossings in the given time-value signal.
	<t:float> <v:float> ...
	help                    Prints this message.
	exit                    Exits the program."""
	)

	return True



def run_command(command: list[str]) -> bool:
	return try_commandspecs(
		[
			CommandSpec(
				[
					Rule([Transform(int, 0)])
				],
				print_crossing
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
