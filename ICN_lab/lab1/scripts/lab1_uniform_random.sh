#!/bin/bash

# init
value=0.02      # loop times
echo "average packet latency" > m5out/uniform_random.txt

# loop
for ((i=0; i<=48; i++))
do
    # run simulation and save the result
    ./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py \
    --network=garnet \
    --num-cpus=64 \
    --num-dirs=64 \
    --topology=Mesh_XY \
    --mesh-rows=8 \
    --sim-cycles=1000000 \
    --inj-vnet=0 \
    --injectionrate=$value \
    --synthetic=uniform_random

    grep "average_packet_latency" m5out/stats.txt | awk '{print $2}' >> m5out/uniform_random.txt
    # grep "average_packet_latency" m5out/stats.txt | sed 's/system.ruby.network.average_packet_latency\s*/average_packet_latency = /' >> m5out/uniform_random.txt
 
    # value = value + 0.02
    value=$(echo "$value + 0.02" | bc)
done
