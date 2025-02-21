# CECS 427 PROJECT 2: SOCIAL AND LARGE-SCALE NETWORKS
#### Written by: Chi Vo
#### Date: February 21, 2025

This is a class project from CECS 427 at California State University Long Beach, instructed by Dr. Oscar Morales Ponce. 

### Objective
Using Python and its libraries (e.g., Matplotlib, Networkx) to calculate and illustrate cluster coefficients and neighborhood overlaps within an input graph. 

### How to run the code?
Along with typing the input graph (in .gml format), there are 5 parameters that can be used to run this program.

`-- components [n = number of components]`: This parameter divides the graph into n subgraphs or clusters using the Networkx built-in function `edge_betweenness_partition()`


`-- plot [C|N|P]`: This parameter decides how the graph will be plotted based on the choices C, N, and P.

- C: The graph will highlight the clustering coefficients of nodes -- the node size is directly proportional to the clustering coefficient, and the node color demonstrates the degree of a node, as the color blue will be applied to nodes with the lowest degree, to magenta for nodes with the highest degree. 
- N: The graph will be plotted with neighborhood overlap values of its edges. When choosing this option, click on a node and it will draw a BFS tree starting from that node.
- P: The graph will be plotted with the node color according to the attribute, or the default color if the color is not assigned.


`--verify_homophily`: This parameter checks if there is evidence of homophily.


`--verify_balanced_graph`: This parameter checks if the graph is balanced.


`--output [file name in .gml format]`: Create an output .gml file and save it at user's current directory. 



_Examples_:

`python ./graph_analysis.py graph_file.gml --components 3 --plot CN --output out_graph_file.gml`: 
Read graph_file.gml and partition it into 3 connected components, plot the graph and highlight the clustering coefficient, and save the graph in out_graph_file.gml. 


`python ./graph_analysis.py homophily.gml --plot P --verify_homophily `: 
Read homophily.gml, plot the graph and verify if there is evidence of homophily in the graph.


`python ./graph_analysis.py balanced_graph.gml --plot P --verify_balanced_graph`:
Read balanced_graph.gml, plot the graph and verify if the graph is balanced. 


