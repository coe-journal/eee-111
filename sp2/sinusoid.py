# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass

import math



@dataclass
class Arguments:
	@classmethod
	def from_str(cls, frequency: str, duration: str, points: str, show: str) -> "Arguments":
		return Arguments(float(frequency), float(duration), int(points), show == "true")

	frequency: float
	duration: float
	points: int
	show: bool



def input_list(prompt: str) -> list[str]:
	return [s for s in input(prompt).split()]

def input_args(prompt: str) -> Arguments:
	split = input_list(prompt)
	return Arguments.from_str(*split)



def __main__():
	args = input_args("> ")
	print(args)



__main__()
