# Project Overview

This project aims to find a design for a 3-string instrument/arc in terms of the tensions (τ), lengths (l), mass densities (μ), and center of mass that produces a set of strictly odd "harmonics." <br>
The primary focus is on achieving the first 5 harmonics.

## Derivations of Ratios

[Derivations_of_Ratios.pdf](Derivation_of_Ratios.pdf) is a short derivation for the ratios of tensions (τ₁, τ₂, τ₃) in terms of angles θ and γ.

## design.py

`design.py` is a design class that provides you with the spectral equation of a design given a set of parameters<br>
It can find the roots, plot them, and return a percentage error to the expected harmonics ([1,3,5,7,9]). <br>
To run this file, you need a few Python libraries: matplotlib, pychebfun, and numpy. <br>
These can be installed with the following commands:

```sh
pip install matplotlib
pip install pychebfun
pip install numpy
```
To run this program, simply type:
```sh
python3 design.py
```
## guess.py


`guess.py` is a hill climbing algorithm (SPSA) used to attempt to find the best design. <br>
It randomly generates a design to start with (you can provide one via file input as well), and then uses a bitmask to determine which direction to proceed in! 
<br> This file requires `design.py` and all of its imports. 
<br>No additional imports are required. Running it is as simple as typing:
```sh
python3 guess.py
```
## SPSA.py

`SPSA.py` is similar to `guess.py`, but instead of using a bitmask to determine the direction, it only has two directions, all negative or all positive (0b000... or 0b1111...). <br>
The same imports are required, and to run it, you do:

```sh
python3 SPSA.py
```
Please make sure to have all the necessary files and libraries installed before running the programs. Happy harmonics designing!
