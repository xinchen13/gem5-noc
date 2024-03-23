#!/bin/bash

# init
value=0.02      # loop times
echo "average packet latency" > m5out/mesh_uniform_random.txt
echo "average packet latency" > m5out/flattenedbutterfly_uniform_random.txt
echo "average packet latency" > m5out/mesh_tornado.txt
echo "average packet latency" > m5out/flattenedbutterfly_tornado.txt
echo "average packet latency" > m5out/mesh_neighbor.txt
echo "average packet latency" > m5out/flattenedbutterfly_neighbor.txt

# loop
for ((i=0; i<=48; i++))
do
    # mesh + uniform_random
    ./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py \
    --network=garnet \
    --num-cpus=16 \
    --num-dirs=16 \
    --topology=Mesh_XY \
    --mesh-rows=4 \
    --sim-cycles=5000000 \
    --inj-vnet=0 \
    --router-latency=2 \
    --injectionrate=$value \
    --synthetic=uniform_random \
    --link-width-bits=32
    grep "average_packet_latency" m5out/stats.txt | awk '{print $2}' >> m5out/mesh_uniform_random.txt

    # flattenedbutterfly + uniform_random
    ./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py \
    --network=garnet \
    --num-cpus=16 \
    --num-dirs=16 \
    --topology=FlattenedButterfly \
    --mesh-rows=4 \
    --sim-cycles=5000000 \
    --inj-vnet=0 \
    --router-latency=2 \
    --injectionrate=$value \
    --synthetic=uniform_random \
    --link-width-bits=32
    grep "average_packet_latency" m5out/stats.txt | awk '{print $2}' >> m5out/flattenedbutterfly_uniform_random.txt

    # mesh + tornado
    ./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py \
    --network=garnet \
    --num-cpus=16 \
    --num-dirs=16 \
    --topology=Mesh_XY \
    --mesh-rows=4 \
    --sim-cycles=5000000 \
    --inj-vnet=0 \
    --router-latency=2 \
    --injectionrate=$value \
    --synthetic=tornado \
    --link-width-bits=32
    grep "average_packet_latency" m5out/stats.txt | awk '{print $2}' >> m5out/mesh_tornado.txt

    # flattenedbutterfly + tornado
    ./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py \
    --network=garnet \
    --num-cpus=16 \
    --num-dirs=16 \
    --topology=FlattenedButterfly \
    --mesh-rows=4 \
    --sim-cycles=5000000 \
    --inj-vnet=0 \
    --router-latency=2 \
    --injectionrate=$value \
    --synthetic=tornado \
    --link-width-bits=32
    grep "average_packet_latency" m5out/stats.txt | awk '{print $2}' >> m5out/flattenedbutterfly_tornado.txt

    # mesh + neighbor
    ./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py \
    --network=garnet \
    --num-cpus=16 \
    --num-dirs=16 \
    --topology=Mesh_XY \
    --mesh-rows=4 \
    --sim-cycles=5000000 \
    --inj-vnet=0 \
    --router-latency=2 \
    --injectionrate=$value \
    --synthetic=neighbor \
    --link-width-bits=32
    grep "average_packet_latency" m5out/stats.txt | awk '{print $2}' >> m5out/mesh_neighbor.txt

    # flattenedbutterfly + neighbor
    ./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py \
    --network=garnet \
    --num-cpus=16 \
    --num-dirs=16 \
    --topology=FlattenedButterfly \
    --mesh-rows=4 \
    --sim-cycles=5000000 \
    --inj-vnet=0 \
    --router-latency=2 \
    --injectionrate=0.02 \
    --synthetic=neighbor \
    --link-width-bits=32
    grep "average_packet_latency" m5out/stats.txt | awk '{print $2}' >> m5out/flattenedbutterfly_neighbor.txt

    # value = value + 0.02
    value=$(echo "$value + 0.02" | bc)
done
