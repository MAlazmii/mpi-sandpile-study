# Evidence and method

## What is in the archive

The original is the author's 2025–26 University of Edinburgh MSc
Message-Passing Programming coursework. The investigation covered C/MPI
Cartesian decomposition and halo exchange for an integer toppling model.
The recovered ARCHER2 2-D solver, header, image writer, Makefile and 15
job scripts match their counterparts inside the submitted ZIP byte for
byte, as do the 15 historical logs. The image writer also matches the
provided teaching starter.
This repository contains original case-study prose, a plotting script and
scalar measurements derived from the archived runs. Coursework source,
handouts, logs and images are retained in the original local archive.

## How the historical records were checked

Each CSV row comes from one saved log. The record column gives the source
record stem. The audit checked the process-grid product, the dimensions of
each local block, the initial and final grain totals, final minimum and
maximum heights, iteration count and total runtime. The submitted report
identifies ARCHER2 and a Cray compiler with `-O3`. The exact producing
binary for each run, compiler version and repeat runs were unavailable.

The saved solver measures the fixed iteration loop between MPI barriers.
The loop includes per-iteration halo exchange, global change-count
reduction, copying the updated local grid and periodic progress messages.
The final validation, global gather and image output follow the timer.
The reported total divided by 655,360 agrees with each logged per-step
time to the displayed precision.

### Fixed 512 × 512 grid

The eight archived records use one to 128 ranks, 524,288 initial grains
and 510,178 final grains. The submitted report identifies one compute node
for this series. The reported runtime falls from 783.903493 to 19.477061
seconds. This is a 40.25× ratio for the recorded workload, equivalent to
31.4% parallel efficiency at 128 ranks when normalised to the one-rank
timing. Single samples give no estimate of run-to-run variation.

The saved final heights range from zero to three, and the eight images
have identical file hashes. The image writer clips values above three.
The hashes therefore corroborate the printed ranges but cannot, on their
own, distinguish unstable heights from height three.

### Varying grid and node placement

Most varying-grid cases give each rank 256 × 256 cells. At 32 ranks the
8 × 4 process grid gives 192 × 384 cells per rank, or 73,728 cells.
That is 12.5% more than 65,536 cells, so the series is an approximate
weak-scaling workload. The recorded initial pile is 100,000 grains for
every case. The submitted implementation initialises twice the number of
global cells. The CSV records both counts so the provenance difference
is visible. All five cases report a final maximum of three.

The placement records keep the grid at 3,072 × 3,072 and 128 ranks, with
one node at 128 ranks per node or two nodes at 64 ranks per node. Each
log starts with 9,437,184 grains. The same submitted formula would give
18,874,368. Both logs end at a maximum height of 8,828,872 and record the
solver's above-threshold diagnostic. The reported two-node runtime is
3.7% lower in this pair of samples. These measurements cover a fixed
iteration budget on an unstable endpoint. No hardware counters, affinity
records or repeats establish a causal explanation for the difference.
The archived implementation reports unstable heights but can still exit
successfully. A zero exit status alone gives no evidence of stability.

## Independent full-grid check

The local comparison used the archived 2-D source and a separate serial
reference. The reference iterates over toppling cells and scatters their
grains into a new grid. It counts each grain that crosses an open edge.
This differs from the MPI solver's stencil, which gathers increments
from neighbour heights after halo exchange.

For the temporary build, set the iteration bound to the case count and
link a replacement output function that writes every gathered integer
height in row order. Leave the update, communication and gather logic
intact. Initialise a single pile of twice the number of grid cells at
the same row and column offset in both models. The original source hash
is recorded in the JSON alongside build flags and environment.

The tested cases cover 8 × 8 grids with offsets zero and four, and a
2 × 2 grid with four ranks. Runs use one, 16 or 256 synchronous iterations.
For example, after one iteration on the 8 × 8 corner pile, 124 grains
remain at the original cell, the adjacent interior row receives one,
and both horizontal neighbours receive one. The left neighbour wraps
to the final column and one grain leaves through the top boundary.
Every tested grid matches the reference, and its total equals the
initial pile less the independently counted escapes.

The local runtime used Open MPI 5.0.6 under x86_64 translation on an
Apple M1. These are small correctness checks. They leave larger-grid,
native Linux and cluster verification open. The released data supports
independent figure generation. Rebuilding the historical solver requires
access to the retained coursework archive.
