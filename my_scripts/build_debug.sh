#!/bin/bash

# path
folder_to_check="./build/Garnet_standalone"

if [ -d "$folder_to_check" ]; then
    echo "deleting existing build dir..."
    rm -rf "$folder_to_check"
    
    echo "done"
else
    echo "no existing build dir"
fi

scons ./build/Garnet_standalone/gem5.debug PROTOCOL=Garnet_standalone -j8
