# DPDPTW Framework

This project aims to allow easier modifications for adapting to different problems or solution methods for dynamic routing problems class with time windows and pickup and delivery.

The algorithm implemented for solving the problem was inspired by Sartori & Buriol 2020.

## Installation

Download the code via git:

```
git clone https://github.com/thuzax/vrp-solver/edit/dev
```

Install python packages:

```
pip install -r requirements.txt
```

Download and install [CBC](https://www.coin-or.org/Cbc/) or [Gurobi](https://www.gurobi.com/) Solver.


## Directories Structure

The [solver](https://github.com/thuzax/vrp-solver/tree/dev/solver) is the main directory of this project. There can be found the solver implementation.

Other files and directories were created for experiments and solution verification.

## Reproducing experiments

Expertiments with the framework were conducted. The instances can be found [here](https://drive.google.com/drive/folders/1MaluGrBbSeZxU6YqHV7_TlU1VfTCQbWj?usp=sharing) and results can be found [here](https://drive.google.com/drive/folders/19peJUvOsI_D450W_X6xf2Kob5r8V5dIZ?usp=sharing).

To reproduce our results first go set the problem configuration file in the [server directory](https://github.com/thuzax/vrp-solver/tree/dev/server_solver) by editing the [json configuration file list](https://github.com/thuzax/vrp-solver/blob/dev/server_solver/configuration_file_list.json).

For each problem this file sets a configuration file. Our experiments were conducted with "DPDPTWNoC-D" (for Dynamic Pickup and Delivery Problem with Time Windows - DPDPTW)  and "DPDPTWHF-R" (for Dynamic Pickup and Delivery Problem with Time Windows with Urban and Rural Points - DPDPTW/UR). The configuration files for reproduction can be found [here](https://github.com/thuzax/vrp-solver/tree/dev/server_solver/configurations). 

For DPDPTW considering an unlimited non-capacitaded fleet we conducted experiments with two insertion algorithms in the constructive phase. The fist considers a [configuration file with first feasible insertion](https://github.com/thuzax/vrp-solver/blob/dev/server_solver/configurations/config_dpdptw_no_cap_with_ages.json) and the second uses a [configuration file with k-regret](https://github.com/thuzax/vrp-solver/blob/dev/server_solver/configurations/config_dpdptw_no_cap_with_ages_k_regret.json). The DPDPTW/UR was also solved with [first feasible insertion](https://github.com/thuzax/vrp-solver/blob/dev/server_solver/configurations/config_dpdptw_no_cap_with_ages_heter_fleet.json) and [k-regret](https://github.com/thuzax/vrp-solver/blob/dev/server_solver/configurations/config_dpdptw_no_cap_with_ages_k_regret_heter_fleet.json).

**Important**: Our experiments were conducted with Gurobi solver. If your experiments will use the CBC the results can be different. Additionally, the "sovler_code" key of "SetPartitionModel" entry must be changed to "CBC" in the related configuration file.

With the configuration files defined, the test server can be initialized. In [server_solver](https://github.com/thuzax/vrp-solver/tree/dev/server_solver) directory execute the following command:

```
python server_solver.py
```

While running the server, in the main directory, execute the [run_tests.py](https://github.com/thuzax/vrp-solver/blob/dev/run_tests.py) file:

```
python run_tests.py <inputs-directory> <output-direcotory> <problem-code>
```

The <inputs-directory> is a directory containing the instances. The <output-directory> is were the solutions must be stored. Finally, the <problem-code> is the code for the solving problem, being "DPDPTWNoC-D" for DPDPTW and "DPDPTWUR-R" for DPDPTW/UR.

## References

SARTORI, Carlo S.; BURIOL, Luciana S. A study on the pickup and delivery problem with time windows: Matheuristics and new instances. Computers & Operations Research, v. 124, p. 105065, 2020.

## Authors

[Arthur Henrique Sousa Cruz](https://github.com/thuzax/)

[Mayron César de Oliveira Moreira](https://github.com/mayronmoreira)

[Miguel Rodrigues](https://github.com/ElMigu17)

[Franklina Maria Bragion de Toledo](https://sites.icmc.usp.br/fran/wiki/pmwiki.php)
