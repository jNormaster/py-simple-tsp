# -*- coding: utf-8 -*-
"""
Created on September 2015
@author: JNorMaster (Jens N.)

Summary: Solving the traveling salesman problem with three construction algorithms.
Algorithms used: Random, Iterative Random and Greedy. 
All algorithms are tested/improved with Greedy Improved.

This code uses a complete graph (all cities are connected)
"""

# Libraries used for this program
from pylab import *
import random as rnd
import copy
import matplotlib.pyplot as plt


##                  ##
## Graph generation ##
##                  ##

def randomCompleteGraph( numCities ):
    
    #Makes a nested list - same as a NxM matrix
    complete_graph = [ [ 0 for i in range( numCities ) ] for j in range( numCities ) ]
    
    #For number of cities, make a random distance between them
    #Each row represent a city, and each column in that row represent the distance to the other cities
    for row in range( numCities ):
        for col in range( numCities ):
            
            #Distance is set to a random number between 1 - 10
            complete_graph[ row ][ col ] = rnd.randrange( 1, 10 )
            
            #Symmetry in the matrix - the distance from A to B is equal to the distance from B to A
            if row > col:
                complete_graph[ row ][ col ] = complete_graph[ col ][ row ]
            
            #Distance is 0 to its own city
            elif row == col:
                complete_graph[ row ][ row ] = 0
 
    return complete_graph
    
##             ##
## Swap Method ##
##             ##
  
def swap_two_random( pathI ):
    
    #copies the input path to swap_path
    swap_path = copy.deepcopy(pathI)
    
    #Chooses two random numbers (indexes) in the path
    n = rnd.randrange(0, len(pathI) )
    m = rnd.randrange(0, len(pathI) ) 
    
    #Swapping their positions
    tmp = swap_path[n]
    swap_path[n] = swap_path[m]
    swap_path[m] = tmp
     
    return swap_path

##                      ##
## Distance calculation ##
##                      ##
 
def calculate_total_distance( graphI, pathI ):

    tot_distance = 0
    
    #for number of cities in the path, calculate the distance, e.g. from A - B - C - D
    for c in range( 1, len( pathI ) ):
        tot_distance = tot_distance + graphI[ pathI[c-1] ][ pathI[c] ]
    
    #Adding the distance going home, e.g. from D - A
    tot_distance = tot_distance + graphI[ pathI[0] ][ pathI[len(pathI) - 1] ] 

    return tot_distance

##                        ##
## Find min number in row ##
##                        ##
 
def find_min_numb_in_row( row, graphI ):
    
    #Used to find the shortest distance e.g. from city A (row 0)
    row_min = graphI[row][0]
    
    for i in range(len(graphI)):
        #skip the columns with 0 (illegal destionation)       
        if row_min == 0:
            row_min = graphI[row][i]
    
    num_index = graphI[row].index( row_min )
    
    #for number of cities legal to travel to - gives the index of the shortest distance to a city
    for col in range( 1, len(graphI) ):
        if row_min > graphI[row][col] and graphI[row][col] > 0:
            row_min = graphI[row][col]
            num_index = graphI[row].index(row_min)
     
    return num_index

###############################
### Construction Algorithms ###
###############################  

##              ##
##    Random    ##
##              ##
 
def random_alg( graphI ):
    
    #makes a list visit with 0s (no cities visited)
    visit = [0] * len( graphI ) 
    random_path = []
    
    #picks a random start city
    start_city = rnd.randrange( 0, len( graphI ) )
    
    #appends it to the random path, and sets the index of that city in visit to 1 (the city is visited)
    random_path.append( start_city )
    visit[ start_city ] = 1
    
    #while not all cities are visited
    while 0 in visit:
        
        #pick a new random city and append it as long as its not in the random path, and mark it visited       
        new_city = rnd.randrange( 0, len( graphI ))
        
        if new_city not in random_path:
            random_path.append( new_city )
            visit[ new_city ] = 1             
     
    return random_path

##                   ##
## Iterative Random  ##
##                   ##
 
def iter_random_alg( graphI, iterations ):
    
    #makes a random path as start path
    start_path = random_alg( graphI )
    start_distance = calculate_total_distance( graphI, start_path )     
 
    #Setting random start path as the shortest distance
    min_path = start_path
    min_distance = start_distance
     
    #Do number of iterations to see if new random path has shorter distance
    while iterations > 0:    
         
        iter_path = random_alg( graphI )        
        iter_distance = calculate_total_distance( graphI, iter_path )
        
        #If the new random path has shorter distance set it as the min distance and path
        if iter_distance < min_distance:
            min_distance = iter_distance
            min_path = iter_path
             
        iterations -= 1
         
    return min_path

##          ##
##  Greedy  ##
##          ##
 
def greedy_alg( graphI ):
 
    graph_copy = copy.deepcopy( graphI )
    greedy_path = []
    
    #fills the list visit with zeros (no cities visited)
    visit = [0] * len( graph_copy )
    
    #pick a random start city and append it to the greedy path and mark it visited
    start_city = rnd.randrange( 0, len( graph_copy ) )
    greedy_path.append( start_city )        
    visit[ start_city ] = 1 
    
    #sets the start city as the current city
    current = start_city
    
    #While not all cities are visited
    while 0 in visit:
        
        #from the current city find the neighbor with the shortest distance
        find_closest_neighbor = find_min_numb_in_row(current, graph_copy)
        
        #if that city is not in the path - append it to the greedy path and mark it visited
        if find_closest_neighbor not in greedy_path:
            greedy_path.append( find_closest_neighbor )
            visit[ find_closest_neighbor ] = 1
        
            #make sure you cannot visit same city again
            for i in range(len(graph_copy)):
                graph_copy[current][i] = 0
                graph_copy[i][current] = 0
                
        current = find_closest_neighbor
    return greedy_path

##                   ##
##  Greedy Improved  ##
##                   ##

def greedy_improved_alg( graphI, pathI ):
    
    orig_pathDist = calculate_total_distance(graphI, pathI)
    
    new_pathDist = copy.copy(orig_pathDist) 
    new_path = copy.copy(pathI)    
    
    result = []
    xval = []
    num_of_runs = 0
    counter_same_num = 0
    
    while 1:
        
        #appends the number of runs/iterations to a list (used for plotting)
        xval.append(num_of_runs)

        #appends the result of the greedy improved distance to result list      
        result.append(new_pathDist)
        
        swapPath = copy.copy(swap_two_random(new_path))        
        swapDist = calculate_total_distance(graphI, swapPath)

        #if distance from the swapped path is improved or the same it will be set as the new path
        if swapDist < new_pathDist:
            new_path = copy.copy(swapPath)
            new_pathDist = copy.copy(swapDist)
            counter_same_num = 0 #shorter distance found so counter is reseted
        
        #if the distance is the same accept the new path
        elif swapDist == new_pathDist:
            new_path = copy.copy(swapPath)
            new_pathDist = copy.copy(swapDist)
            counter_same_num += 1  
         
        #if distance from swapping has greater distance, skip it and start over
        elif swapDist > new_pathDist:
            counter_same_num += 1

        num_of_runs += 1
        
        #change these values for different stopping criteria
        if counter_same_num == 1000 or num_of_runs == 500000:
            break
    
    return xval, result, new_path

############
### Main ###
############
    
if __name__ == "__main__":

    numCities = int(raw_input("number of cities: "))
    myGraph = randomCompleteGraph( numCities )
    
    while (1):    
        min_list = []
        max_list = []
        index_best_path = None
        tours = []
        tot = 0
        
        algChoice = int(raw_input("1 for random\n2 for random iterative\n3 for greedy\n4 for exit\n: "))         
        
        #Run Random algorithm and greedy improved
        if algChoice == 1:
        	
            num_of_runs = int(raw_input("How many times to run random & greedy improve?: "))

            for i in range(num_of_runs):

              rndPath = random_alg( myGraph )
              gI_val, gI_res, path_found = greedy_improved_alg(myGraph, rndPath)    
              tours.append(path_found)
              
              min_list.append(min(gI_res))
              max_list.append(max(gI_res))            

              #            x-min ,     x-max                ,   y-min                       ,    y-max
              plt.axis([gI_val[0], gI_val[ len(gI_val) - 1 ], gI_res[ len(gI_res) - 1 ] - 10, gI_res[0] + 50 ])
              gI_val = array(gI_val)
              plt.plot(gI_val, gI_res)
            plt.title("Random with GI")
            plt.show()
            
            for k in range(len(min_list)):
                tot += max_list[k] + min_list[k]
            avg = tot / len(min_list)
            print "Average distance among all (" + str(num_of_runs) + ") tours:", avg
            
            index_best_path = min_list.index(min(min_list))
            dist_shortest_tour = calculate_total_distance(myGraph, tours[index_best_path])
            tours[index_best_path].append(tours[index_best_path][0]) #adding homecity to list in last position
            print "The Shortest tour:", tours[index_best_path]
            print "Distance: ", dist_shortest_tour
            
            #resetting before next run            
            min_list = 0
            max_list = 0
            tours = 0
	
        #Run Random iterative algorithm
        elif algChoice == 2:
            
            num_of_runs = int(raw_input("How many times to run random iterative & greedy improve?: "))
            
            #if user should be asked for number of iterations for random iterative
            #iterations = int(raw_input("number of iterations: "))
            
            #number of iterations is set to 5, comment out if want to use user specified instead
            iterations = 5
            
            for i in range(num_of_runs):
              
              iterRndPath = iter_random_alg( myGraph, iterations )
              gI_val, gI_res, path_found = greedy_improved_alg( myGraph, iterRndPath)
              
              tours.append(path_found)  
              min_list.append(min(gI_res))
              max_list.append(max(gI_res)) 
              
              #            x-min ,     x-max                ,   y-min                       ,    y-max 
              plt.axis([gI_val[0], gI_val[ len(gI_val) - 1 ], gI_res[ len(gI_res) - 1 ] - 10, gI_res[0] + 5 ])
              plt.plot(gI_val, gI_res)
            plt.title("Iterative Random with GI")
            plt.show()
            
            for k in range(len(min_list)):
                tot += max_list[k] + min_list[k]
            avg = tot / len(min_list)
            print "Average distance among all tours:", avg
            
            index_best_path = min_list.index(min(min_list))
            dist_shortest_tour = calculate_total_distance(myGraph, tours[index_best_path])           
            tours[index_best_path].append(tours[index_best_path][0]) #adding homecity to list in last position
            print "The Shortest tour:", tours[index_best_path]
            print "Distance: ", dist_shortest_tour
            
            #resetting before next run            
            min_list = 0
            max_list = 0
            tours = 0
            
        #Run Greedy algorithm
        elif algChoice == 3:
                 
            num_of_runs = int(raw_input("How many times to run greedy & greedy improve?: "))
            
            for i in range(num_of_runs):
              greedyPath = greedy_alg( myGraph )
              gI_val, gI_res, path_found = greedy_improved_alg( myGraph, greedyPath) 
   
              tours.append(path_found)
            
              min_list.append(min(gI_res))
              max_list.append(max(gI_res))            
              
              #            x-min ,     x-max                ,   y-min                       ,    y-max
              plt.axis([gI_val[0], gI_val[ len(gI_val) - 1 ], gI_res[ len(gI_res) - 1 ] - 10, gI_res[0] + 5 ])
              plt.plot(gI_val, gI_res)
            plt.title("Greedy with GI")
            plt.show()
            
            for k in range(len(min_list)):
                tot += max_list[k] + min_list[k]
            avg = tot / len(min_list)
            print "Average distance among all tours:", avg
            
            index_best_path = min_list.index(min(min_list))
            dist_shortest_tour = calculate_total_distance(myGraph, tours[index_best_path])
            tours[index_best_path].append(tours[index_best_path][0]) #adding homecity to list in last position
            print "The Shortest tour:", tours[index_best_path] 
            print "Distance: ", dist_shortest_tour 
            
            #resetting before next run
            min_list = 0
            max_list = 0
            tours = 0
            
        #exit the program
        elif algChoice == 4:
            break

    print "Thanks for running this program!"