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

def derivative(x: list[float], y: list[float]) -> list[float]:
	"""
	Generates a list of floats corresponding to the slope of each consecutive pair of x and y coordinates.
	"""
	d = [0.0]
	for i in range(1, len(x)):
		dx = x[i] - x[i - 1]
		dy = y[i] - y[i - 1]
		d.append(dy / dx)
	return d

def integral(x: list[float], y: list[float]) -> list[float]:
	"""
	Generates a list of floats corresponding to the area below the function from zero to every x coordinate.
	"""
	I = [0.0]
	accum = 0.0
	for i in range(1, len(x)):
		dx = x[i] - x[i - 1]
		accum += dx * y[i]
		I.append(accum)
	return I

def factor(l: list[float], a: float) -> list[float]:
	"""
	Multiplies all elements in the list by a factor a.
	"""
	return [a * lx for lx in l]

def add(a: list[float], b: list[float]) -> list[float]:
	"""
	Returns a list of floats corresponding to the element-wise sums of a and b.
	"""
	return [a + b for a, b in zip(a, b, strict=True)]

def cos_wave(t: list[float], a: float, f: float) -> list[float]:
	"""
	Generates a cosine wave with a list of timepoints , an amplitude, and a frequency.
	"""
	return [a * math.cos(2 * math.pi * f * tx) for tx in t]



def __main__():
	# Answer to the question:
	# We can see that the Vpp across the input is at its lowest around f=460 Hz, 0.011 Vpp.
	# This is because the resonant frequency of the circuit is also 460 Hz. More specifically,
	# if we calculate f_r = \frac{1}{2\pi\sqrt{LC}}, the result is 459.44074. Thus, we can
	# conclude that the Vpp of an RLC circuit undergoes a sudden drop until it reaches the
	# resonant frequency of the circuit, after which, the Vpp will gradually increase again.

	pp = 0.001
	frequencies = range(100, 10000 + 1)
	amplitude = pp / 2
	resistance = 1
	inductance = 0.120
	capacitance = 0.000001

	data = []

	for frequency in frequencies:
		t = frange(0, 0.01, 1000)
		cos = cos_wave(t, amplitude, frequency)
		vr = factor(cos, resistance)
		vl = factor(derivative(t, cos), inductance)
		vc = factor(integral(t, cos), 1 / capacitance)
		vs = add(add(vr, vl), vc)
		vpp = max(vs) - min(vs)
		data.append(vpp)

	figure, axis = plot.subplots()
	axis.plot(frequencies, data)
	plot.show()



__main__()
