# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import math

import matplotlib.pyplot as plot



def frange(start: float, stop: float, samples: int) -> list[float]:
	"""
	Generates a list of floats in the interval (start, stop) with a fixed step, (stop - start) / samples.
	"""
	step = (stop - start) / samples
	out: list[float] = []
	for i in range(0, samples):
		out.append(start + step * i)
	return out

def cos_wave(t: list[float], f: float) -> list[float]:
	"""
	Generates a cosine wave with a list of timepoints and a frequency.
	"""
	return [math.cos(2 * math.pi * f * tx) for tx in t]



def __main__():
	t = frange(0, 0.001, 1000)
	cos = cos_wave(t, 10000)

	figure, axis = plot.subplots()
	axis.plot(t, cos)
	plot.show()



__main__()
