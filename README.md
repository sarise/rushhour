Rush Hour!
=========
 
Rush Hour is a tiny sliding board game played on a board of 6x6 squares.
The objective in the game is to free the red car from the surrounding traffic by sliding the cars out of the way onto free squares until the red car can drive out of the exit on the right side of the board. Note that cars can only go forward or reverse, not to the side. Use google or this video for an impression:
 
http://www.youtube.com/watch?v=yuoYbb1fR5Q
 
We would like you to build a solver for the game! The input could be a text-based level description like so:
 
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
 
In this input A through J represent the cars and rr is the red car that needs to be freed. The output should be a sequence of moves like A-up, B-down, etc. etc.

The proposed solution is to utilise breadth first search (BFS). 
