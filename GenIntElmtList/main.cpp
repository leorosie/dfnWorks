#include <vector>
#include <fstream>
#include <iostream>
#include "linkedList.h"
#include "parseInputFunctions.h"
#include "lineConnection.h"
#include "tri.h"

// Comment/Uncomment for debug prints
//#define DEBUG

// Comment/Uncomment to display all node disconnect pairs before exiting
//#define CHECKALLNODES


/*************************************************************************************/
// Tests whether or not the intersection connectivity passed to lagrit still 
// exists after lagrit has meshed the fracture.
// cmd line args: 
// Arg 1: Path to fracture intersection inp file
// Arg 2: Path to intersection node to global node numbers file.
// Arg 3: Path to mesh inp file
// Return: 0 - All connections present, test passed successfully.
//         Anything not 0 - test failed, found unconnected nodes which should be connected
int main(int argc, char **argv) {
    
    using namespace std;

    //check cmd line args
    if (argc != 5) {
        cout <<"\nMust inlude cmd line arguments:\n";
        cout << "Arg 1: Path to fracture intersection inp file.\n";
        cout << "Arg 2: Path to intersection node to global node numbers file.\n";
        cout << "Arg 3: Path to mesh inp file \n";
        cout << "Arg 4: Path to output filename\n";

        exit(1);
    }

    #ifdef DEBUG
    cout << "\nIntersections file: " << argv[1] << endl;
    cout << "Global node numbers file: " << argv[2] << endl;
    cout << "Mesh inp file: " << argv[3] << endl;
    cout << "Output folder: " << argv[4[ << endl << endl;
    #endif
    
    int connSize; //connSize is set in readIntersectionConnectivity()
    // read intersection.inp file into array
    LineConnection* connections = readIntersectionConnectivity(argv[1], connSize);
    
    #ifdef DEBUG
    cout << "\nglobal node connections before\n";
    for (int i = 0; i < connSize; i++) {
        cout << "line " << connections[i].a << " " << connections[i].b << endl;
    }
    #endif
    
    // Change from intersection node numbers to global
    // node numbers
    updateToGlobalNodeNums(argv[2], connections, connSize);

    #ifdef DEBUG
    cout << "\nglobal node connections after\n";
    for (int i = 0; i < connSize; i++) {
        cout << "line " << connections[i].a << " " << connections[i].b << endl;
    }
    #endif

    int triSize;
    // min and max node ids seen while reading tri elmts
    // Used for memory allocation and index offset
    int minId, maxId; 
    
    // read mesh.inp's tri elements into array
    Tri* triElmts = readTriElements(argv[3], triSize, minId, maxId); 

    #ifdef DEBUG
    cout << "max: " << maxId << endl;
    cout << "min: " << minId << endl;
    for (int i = 0; i < triSize; i++) {
        cout << "tri " << triElmts[i].a << " " << triElmts[i].b << " " << triElmts[i].c << "\n";     
    }
    #endif

    // Create edge graph
    // Implemented like a sparse matrix but a linked list    
    int edgeGraphSize = maxId - minId + 1;
    LinkedList* edgeGraph = new LinkedList[edgeGraphSize];
    //Caution about memory usage of empty array spots
   

    //populate linked list (edge graph) with tri elements
    //tri elements are sorted a < b < c     
    //this means we need to insert (a,b), (a,c), and (b,c)
    //to get full connectivty graph
    for (int i = 0; i < triSize; i++) {
        
        int index = triElmts[i].a - minId;
        Node* node = new Node(triElmts[i].b, &triElmts[i]);
        edgeGraph[index].append(node);
        
        index = triElmts[i].a - minId;
        node = new Node(triElmts[i].c, &triElmts[i]);
        edgeGraph[index].append(node);

        index = triElmts[i].b - minId;
        node = new Node(triElmts[i].c, &triElmts[i]);
        edgeGraph[index].append(node);
    }
 
    #ifdef CHECKALLNODES
    bool error = false;
    #endif
   
    // check that all connections in connections[] 
    // also exist in edge graph
    for (int i = 0; i < connSize; i++) {
        int searchIdx;
        int searchFor;

        // Use smallest node number as index
        // This allows us to use upper trianglar matrix,
        // and save memory
        if (connections[i].a < connections[i].b) {
            searchIdx = connections[i].a;
            searchFor = connections[i].b;
        }
        else {
            searchIdx = connections[i].b;
            searchFor = connections[i].a;
        }

        // Index Offset
        searchIdx -= minId;

        #ifdef DEBUG
        std::cout << "Searching in idx " << searchIdx << "\n";
        std::cout << "Searching for " << searchFor << "\n";
        #endif

        if (searchIdx >= edgeGraphSize) {
//            #ifdef DEBUG
            std::cout << "ERROR: Attempted to search beyond edge graph's array bounds. " 
                      << "Node connection (" << searchIdx+minId << ", " << searchFor 
                      << ")  does not exist in edge graph.\n";
//            #endif
            delete[] connections;
            delete[] edgeGraph;
            delete[] triElmts;
            return 1;
        }
        


        // Check the list to see if connection exists
        // Returns null if no connection found
        Node* node = edgeGraph[searchIdx].find(searchFor);
        if (node == nullptr) {
            // Clean up
  			std::cout << "Did not find first element for connection (" << searchIdx+minId << ", " << searchFor << ")\n";
            
            #ifdef CHECKALLNODES
            error = true;
            #else
            delete[] connections;
            delete[] edgeGraph;
            delete[] triElmts;
            return 1;
            #endif
        }
        else {
            node->tri->onIntersection = true;
        }

        // There are two entreis for each pair of nodes or a connection. One for each Tri Element
        // Find the next one and mark it as being on intersection as well.
        node = node->next;
        while (node->id != searchFor &&  node != nullptr) {
            node = node->next;
        }
        if (node == nullptr) {
            // Clean up
  			std::cout << "Did not find second element for connection (" << searchIdx+minId << ", " << searchFor << ")\n";
            
            #ifdef CHECKALLNODES
            error = true;
            #else
            delete[] connections;
            delete[] edgeGraph;
            delete[] triElmts;
            return 1;
            #endif
        }
        else {
            node->tri->onIntersection = true;
        }

        
        
        
    }
//    std::cout<<"Intersection connectivity verified.\n";
    // Clean up

    // Write Tri ELement Data, tags elements on intersection with '1'
    std::ofstream file;
    file.open(argv[4], std::ofstream::out | std::ofstream::trunc);
    if (!file.is_open()) {
        std::cout << "Error opening file: " << argv[4] << "\n";
            delete[] connections;
            delete[] edgeGraph;
            delete[] triElmts;
            return 1;
    }
    
    for (int i = 0; i < triSize; i++) {
        std::cout << i+1 << " ";
        if (triElmts[i].onIntersection == true) {
            file << "1\n";
        }
        else {
            file << "0\n";
        }
    }

    file.close();


    delete[] connections;
    delete[] edgeGraph;
    delete[] triElmts;
    
    #ifdef CHECKALLNODES
    if (error == true) {
        return 1;
    }
    #endif
}

