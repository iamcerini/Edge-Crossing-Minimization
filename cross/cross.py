# Andrea Cerini
# 109226255
# CSE 307 HW 2
# DUE FEB 21 2017

# Import the modules
import fileinput
import itertools
import re
import time

# countCrosses counts the number of edge crosses between two layers using a matrix
def countCrosses(Matrix, L1_index, L1_width, L2_width):
    crosses_count = 0
    for L1_node in range(0, L1_index):
        for L2_node in range(0, L2_width):
            #print("Edge 1: %i %i" % (L1_node, L2_node))
            if Matrix[L1_node][L2_node] != 0:
                #print("Edge 1 Found")
                for L1_node_compare in range(0, L1_width):
                    for L2_node_compare in range(0, L2_width):
                        if Matrix[L1_node_compare][L2_node_compare] != 0:
                            #print("Edge 2 Found: %i %i" % (L1_node_compare, L2_node_compare))
                            if ((L2_node > L2_node_compare) and (L1_node < L1_node_compare)):
                                #print("Edge Cross between [%i][%i] and [%i][%i]" % (
                                #L1_node, L2_node, L1_node_compare, L2_node_compare))
                                crosses_count += 1
    #print("Crosses Count: %i" % (crosses_count))
    return crosses_count

# populateMatrix fills in the edge matrix with the edges between two nodes of two different layers. 1 indicates that there is an edge.
def populateMatrix(list_of_edges, layer_a, layer_b):
    matrix = [[0 for x in range(len(layer_a))] for y in range(len(layer_b))]
    for edge in list_of_edges:
        if edge[0] in layer_a:
            matrix[layer_a.index(edge[0])][layer_b.index(edge[1])] = 1
    cross_count = countCrosses(matrix, len(layer_a)-1, len(layer_a), len(layer_b))
    return cross_count

# populatePermutedMatrix fills in the edge matrix with the edges between two nodes of two different layers for a given permutation. 1 indicates that there is an edge.
def populatePermutedMatrix(list_of_edges, layer_a, layer_b, permute_a, permute_b):
    matrix = [[0 for x in range(len(layer_a))] for y in range(len(layer_b))]
    for edge in list_of_edges:
        if edge[0] in permute_a:
            matrix[permute_a.index(edge[0])][permute_b.index(edge[1])] = 1
    cross_count = countCrosses(matrix, len(layer_a)-1, len(layer_a), len(layer_b))
    return cross_count

# printMatrix is a helper function for printing a matrix
def printMatrix(m):
   for row in m:
    print(row)

def main():
    # PARSE THE INPUTS FROM THE FILES
    list_of_layers = []
    list_of_edges = []
    index = 0
    number_of_layers = 0
    for line in fileinput.input():
        new_command = ''
        if (re.findall('in_layer', line)):
            #print("IN LAYER")
            new_command = line.replace('in_layer(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            list_of_layers[int(new_command[0])-1].append(new_command[1]) # Insert the node in the node list of the current layer
            index = index + 1
        elif(re.findall('edge', line)):
           # print("EDGE")
            new_command = line.replace('edge(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            list_of_edges.append([new_command[0], new_command[1]])
        elif (re.findall('width', line)):
           # print("WIDTH")
            new_command = line.replace('width(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            list_of_nodes = [] # Create the list of nodes of size width for the new layer
            list_of_layers.append(list_of_nodes) # Add the list of nodes to the list of layers
            index = 0
        elif (re.findall('layers', line)):
            # print("LAYERS")
            new_command = line.replace('layers(', '')
            new_command = new_command.replace(').', '')
            number_of_layers = int(new_command)
    fileinput.close() # Close the file

    # SET THE INITIAL TOTAL CROSS COUNT TO THE GIVEN LAYERS AND NODE POSITIONS
    total_cross_count = 0
    for i in range(number_of_layers - 1):
        total_cross_count = total_cross_count + populateMatrix(list_of_edges, list_of_layers[i], list_of_layers[i + 1])  # Get the cross count for the comparison between the given layers and add it to the total count
    if total_cross_count != 0:  # Optimisation: If the given total cross count is not 0, then check through the permutations. Else, it is already optimised :)
        start_time = time.time()
        # GENERATE THE PERMUTATIONS
        list_of_permutations = [{} for x in range(number_of_layers)] # Create the list of layer permutations
        for i in range(len(list_of_layers)):
            node_permutations = [] # Reset the layer node permutation list
            for node_list in itertools.permutations(list_of_layers[i]):
                node_permutations.append(node_list) # For each permutation in the layer, add it to the node list
            list_of_permutations[i] = node_permutations # Add the list of all node permutations for a given layer to the full list of permutations
        # RUN THROUGH THE PERMUTATIONS
        for p in itertools.product(*list_of_permutations):
            count = 0 # Reset the cross count when running permutations
            for i in range(number_of_layers - 1):
                count = count + populatePermutedMatrix(list_of_edges, list_of_layers[i], list_of_layers[i+1], p[i], p[i+1]) # Get the cross count for the comparison between two layers and add it to the running count
                if count > total_cross_count: # Optimisation: If the count of the first layers already exceeds the total count, do not compute the cross count for the remaining layers for the given permutation
                    break
            if count < total_cross_count: # If the running current cross count is less than our lowest recorded cross count, then update our lowest cross count
                total_cross_count = count
                print(p)
                print(total_cross_count)
            if total_cross_count == 0: # Optimisation: If the total cross count is 0, then do not check any more permutations. We have found an optimised solution
                break

    # OLD SOLUTION FOR ONLY 3 LAYERS
    # for p1 in itertools.permutations(list_of_layers[0]):
    #     for p2 in itertools.permutations(list_of_layers[1]):
    #         # Populate the edge matrix between Layers 1 and 2 and get the cross count
    #         L1_L2_edge_matrix,  L1_L2_cross_count = populatePermutedMatrix(list_of_edges, list_of_layers[0], list_of_layers[1], p1, p2)
    #         for p3 in itertools.permutations(list_of_layers[2]):
    #             # Populate the edge matrix between Layers 2 and 3 and get the cross count
    #             L2_L3_edge_matrix, L2_L3_cross_count = populatePermutedMatrix(list_of_edges, list_of_layers[1], list_of_layers[2], p2, p3)
    #             # Sum the calculated cross counts
    #             count = L1_L2_cross_count + L2_L3_cross_count
    #             if count < total_cross_count: # If new permutation has less cross counts then save the permutation
    #                 total_cross_count = count
    #                 #edge_matrix_1 = L1_L2_edge_matrix[:]
    #                 #edge_matrix_2 = L2_L3_edge_matrix[:]
    #                 #new_node_list_1 = p1
    #                 #new_node_list_2 = p2
    #                 #new_node_list_3 = p3

    # PRINT RESULT
    print("Optimization: %i" % (total_cross_count))

    # HELPER PRINT RESULTS
    # print("\n\n----- RESULTS -----\n")
    print("\n --- %s seconds --- \n" % (time.time() - start_time))
    # list_of_layers[0] = new_node_list_1
    # list_of_layers[1] = new_node_list_2
    # list_of_layers[2] = new_node_list_3
    # print("\nLAYER NODE ORDERING\n")
    # print(list_of_layers[0])
    # print(list_of_layers[1])
    # print(list_of_layers[2])
    # print("\nCROSS MINIMISATION COUNT\n")
    # print(total_cross_count)
    # print("\nMATRIX 1\n")
    # printMatrix(edge_matrix_1)
    # print("\nMATRIX 2\n")
    # printMatrix(edge_matrix_2)

if __name__ == "__main__":
    main()