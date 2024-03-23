# NoC simulation in gem5(a simple tutorial for Garnet)
Run and modify Garnet as a stand-alone in gem5. Garnet models the interconnection network in gem5. It is cyclic accurate, implements the micro-architecture of on-chip router, and uses gem5 ruby memory system for topology and routing

## Purposes
- 熟练使用体系结构模拟器 gem5 进行建模
- 深入理解高性能体系结构的建模，NoC与Cache coherence

## Compile and first run
To run Garnet as a stand-alone, compile it with the following command

```sh
scons build/Garnet_standalone/gem5.debug PROTOCOL=Garnet_standalone -j9
```

Run gem5 using the `garnet_synth_traffic.py` configuration file with default configuration parameters

```sh
./build/Garnet_standalone/gem5.debug configs/example/garnet_synth_traffic.py 
```

## Configuration parameters
In general, all the configurations can be found in `config/` folder. most of the configuration parameters related to Garnet can be found in the following files and folders
- `configs/common/Options.py`: general configration parameters (i.e. number CPUs, directories, memory size, ... etc.)  
- `configs/network/Network.py`: network configuration parameters (i.e. router & link latency, routing algorithm, topology... etc.) 
- `configs/topologies/`: topologies are defined here
- `configs/example/garnet_synth_traffic.py`: template file, include configuration parameters related to a single run (i.e. traffic pattern type, injection rate, number of simulation cycles, ... etc.)

Change any default value of any configuration parameter directly in the related configuration file or change it from command line as follows: `./build/Garnet_standalone/gem5.debug configs/example/garnet_synth_traffic.py [--configuration_name=value]`, e.g.

```sh
./build/Garnet_standalone/gem5.debug configs/example/garnet_synth_traffic.py \
--ruby --ruby-clock=1GHz \
--sys-clock=1GHz \
--mem-type=SimpleMemory \
--num-cpus=16 \
--num-dirs=16 \
--synthetic=bit_complement --injectionrate=0.200 --sim-cycles=100000 --num-packets-max=30000 --inj-vnet=2 \
--network=garnet --topology=Mesh_XY --mesh-rows=4 --vcs-per-vnet=2 --link-latency=1 --router-latency=1 \
--routing-algorithm=1
```

### system configuration
- [--num-cpus=16] number of CPU = 16, the number of source (injection) nodes in the network
- [--num-dirs=16] number of cache directories = 16, the number of destination (ejection) nodes in the network
- [--network=garnet] configure the network as garnet network
- [--topology=Mesh_XY] use `Mesh_XY.py` topology in `configs/topologies/`
- [--mesh-rows=4] number of rows in the network layout

### network configuration
- [--router-latency] number of pipeline stages in the garnet router. Has to be >= 1. Can be over-ridden on a per router basis in the topology file
- [--link-latency] latency of each link in the network. Has to be >= 1. Can be over-ridden on a per link basis in the topology file
- [--vcs-per-vnet=2] number of VCs per vitrual network
- [--link-width-bits] width in bits for all links inside the garnet network. Default = 128.

### traffic injecion
- [--sim-cycles=100000] run simulation for 100000 cycles
- [--synthetic=bit_complement] traffic pattern:  ‘uniform_random’, ‘tornado’, ‘bit_complement’, ‘bit_reverse’, ‘bit_rotation’, ‘neighbor’, ‘shuffle’, and ‘transpose’
- [--injectionrate=0.200] injection rate
- [--num-packets-max] maximum number of packets to be injected by each cpu node. Default value is -1 (keep injecting till sim-cycles)
- [--single-sender-id] only inject from this sender. To send from all nodes, set to -1
- [--single-dest-id] only send to this destination. To send to all destinations as specified by the synthetic traffic pattern, set to -1
- [--inj-vnet] only inject in this vnet (0, 1 or 2). 0 and 1 are 1-flit, 2 is 5-flit. Set to -1 to inject randomly in all vnets

## Garnet source file 
Garnet is written in C++ and uses python to pass the configuration parameters to the C++ objects. All the files are available in `src/mem/ruby/network/garnet/`. In this folder, the NoC and the router micro-architecture is implemented

Scons is a modern software construct tool (similar to Make); it's scripts are written in python. In gem5, any folder that includes a Scons script file will be compiled into gem5 according to the scripts content

Take the Scons script in Garnet folder as an example. This script is located in `src/mem/ruby/network/garnet/Sconscript`. The script is strightforward: to add source file, say `x.cc`, simple add `Source('x.cpp')` in the Scons script

## Debug tips
### Inject one (or more fixed number of) packet(s) into the network from a specific source to a specific destination

This can be done by the following command-line options
```sh
--num-packets-max=<maximum packets to inject> \
--single-sender-id=<sender_id> \
--single-dest-id=<dest_id>
```
e.g.
```sh
./build/Garnet_standalone/gem5.debug configs/example/garnet_synth_traffic.py \
--ruby --ruby-clock=1GHz \
--sys-clock=1GHz \
--mem-type=SimpleMemory \
--num-cpus=16 \
--num-dirs=16 \
--synthetic=bit_complement --injectionrate=0.200 --sim-cycles=100000 --inj-vnet=2 \
--network=garnet --topology=Mesh_XY --mesh-rows=4 --vcs-per-vnet=2 --link-latency=1 --router-latency=1 \
--routing-algorithm=1 \
--num-packets-max=3 --single-sender-id=1 --single-dest-id=7
```

### Print debug messages
Debug messages throughout the Garnet code are in the following format:
`DPRINTF(RubyNetwork, "Debug message is here and is printing value %d", variable)`

We can add our own debug messages across the code to track the progress of a flit. To print the debug messages, add `--debug-flags=RubyNetwork` as follows:

```sh
./build/Garnet_standalone/gem5.debug --debug-flags=RubyNetwork configs/example/garnet_synth_traffic.py \
--ruby --ruby-clock=1GHz \
--sys-clock=1GHz \
--mem-type=SimpleMemory \
--num-cpus=16 \
--num-dirs=16 \
--synthetic=bit_complement --injectionrate=0.200 --sim-cycles=100000 --inj-vnet=2 \
--network=garnet --topology=Mesh_XY --mesh-rows=4 --vcs-per-vnet=2 --link-latency=1 --router-latency=1 \
--routing-algorithm=1 \
--num-packets-max=1 --single-sender-id=1 --single-dest-id=2
```

## Useful scripts
- [build_debug.sh](./my_scripts/build_debug.sh): build Garnet_standalone (debug version)
- [build_opt.sh](./my_scripts/build_opt.sh): build Garnet_standalone (opt version)
- [extract_network_stats.sh](./my_scripts/extract_network_stats.sh) extract network stats

## Advanced labs
Acknowledgment: the labs come from Tushar Krishna, School of ECE, Georgia Institute of Technology, Interconnection Networks for High-Performance Systems (ECE 6115 / CS 8803 - ICN), Spring 2020
- [lab1. Running Synthetic Traffic through a Network](./ICN_lab/lab1/)
- [lab2. Topology Comparison](./ICN_lab/lab2/)
