from m5.params import *
from m5.objects import *

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology

class FlattenedButterfly(SimpleTopology):
    description = 'FlattenedButterfly'

    def __init__(self, controllers):
        self.nodes = controllers

    # Makes a generic FlattenedButterfly assuming an equalt number of cache and
    # directory cntrls
    # Since there will be links of unequal length, therefore thus each link will
    # assign an increasing number of latency based on the distance from it's neighour

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes
        
        # These parameters will be set form the command line
        link_latency = options.link_latency # used by simple and garnet
        router_latency = options.router_latency # only used by garnet
        
        cpu_per_router = 1  # one traffic injector per router
        num_routers = int(options.num_cpus / cpu_per_router)
        num_rows = options.mesh_rows
        
        # There must be an evenly divisible number of cntrls to routers
        # Also, obviously the number of rows must be <= the number of routers
        cntrls_per_router, remainder = divmod(len(nodes), num_routers)
        assert num_rows > 0 and num_rows <= num_routers
        num_columns = int(num_routers / num_rows)
        assert num_columns * num_rows == num_routers

        #  Create the router in the FlattenedButterfly
        routers = [
            Router(router_id=i, latency=router_latency)
            for i in range(num_routers)
        ]
        network.routers = routers

        # print('num_columns: %d' %(num_columns))
        # print('num_rows: %d' %(num_rows))

        # link counter to set unique link ids
        link_count = 0

        # Add all but the remainder nodes to the list of nodes to be uniformly
        # distributed across the network
        network_nodes = []
        remainder_nodes = []
        for node_index in range(len(nodes)):
            if node_index < (len(nodes) - remainder):
                network_nodes.append(nodes[node_index])
            else:
                remainder_nodes.append(nodes[node_index])

        # copy from Mesh_XY.py
        # Connect each node to the appropriate router
        ext_links = []
        for (i, n) in enumerate(network_nodes):
            cntrl_level, router_id = divmod(i, num_routers)
            assert cntrl_level < cntrls_per_router
            ext_links.append(
                ExtLink(
                    link_id=link_count,
                    ext_node=n,
                    int_node=routers[router_id],
                    latency=link_latency,
                )
            )
            link_count += 1

        # Connect the remainding nodes to router 0.  These should only be
        # DMA nodes.
        for (i, node) in enumerate(remainder_nodes):
            assert node.type == "DMA_Controller"
            assert i < remainder
            ext_links.append(
                ExtLink(
                    link_id=link_count,
                    ext_node=node,
                    int_node=routers[0],
                    latency=link_latency,
                )
            )
            link_count += 1
        network.ext_links = ext_links

        # create the FlattenedButterfly links. First row (east-west) links then column (north-south) links
        int_links = []

        # print('creating east(out)-west(in) links:')
        for row in range(num_rows):
            for col in range(num_columns): 
                west_in = col + (row * num_columns)
                for i in range((west_in + 1), (row * num_columns + num_columns)):
                    assert(i < (row * num_columns + num_columns))
                    east_out = i
                    # print("router(" + str(east_out) + ") -> " + "router(" + str(west_in) + ")")
                    int_links.append(IntLink(link_id=link_count,
                                            src_node=routers[east_out],
                                            dst_node=routers[west_in],
                                            src_outport="East",
                                            dst_inport="West",
                                            latency=1,
                                            weight=1))
                    link_count += 1

        # print('creating west(out)-east(in) links:')
        for row in range(num_rows):
            for col in range(num_columns): 
                west_out = col + (row * num_columns)
                for i in range((west_out + 1), (row * num_columns + num_columns)):
                    assert(i < (row * num_columns + num_columns))
                    east_in = i
                    # print("router(" + str(west_out) + ") -> " + "router(" + str(east_in) + ")")
                    int_links.append(IntLink(link_id=link_count,
                                            src_node=routers[west_out],
                                            dst_node=routers[east_in],
                                            src_outport="West",
                                            dst_inport="East",
                                            latency=1,
                                            weight=1))
                    link_count += 1

        # print('creating north(out)-south(in) links:')
        for col in range(num_columns):
            for row in range(num_rows):
                north_out = col + (row * num_columns)
                for i in range(col, north_out, num_columns):
                    south_in = i
                    # print("router(" + str(north_out) + ") -> " + "router(" + str(south_in) + ")")
                    int_links.append(IntLink(link_id=link_count,
                                            src_node=routers[north_out],
                                            dst_node=routers[south_in],
                                            src_outport="North",
                                            dst_inport="South",
                                            latency=1,
                                            weight=2))
                    link_count += 1

        # print('creating south(out)-north(in) links:')
        for col in range(num_columns):
            for row in range(num_rows):
                north_in = col + (row * num_columns)
                for i in range(col, north_in, num_columns):
                    south_out = i
                    # print("router(" + str(south_out) + ") -> " + "router(" + str(north_in) + ")")
                    int_links.append(IntLink(link_id=link_count,
                                            src_node=routers[south_out],
                                            dst_node=routers[north_in],
                                            src_outport="South",
                                            dst_inport="North",
                                            latency=1,
                                            weight=2))
                    link_count += 1
        network.int_links = int_links

    # Register nodes with filesystem
    def registerTopology(self, options):
        for i in range(options.num_cpus):
            FileSystemConfig.register_node(
                [i], MemorySize(options.mem_size) // options.num_cpus, i
            )