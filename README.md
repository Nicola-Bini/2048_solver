<br><br>
<p align="center">
<img width="70%" alt="Screen Shot 2021-09-25 at 1 21 14 PM" src="https://user-images.githubusercontent.com/63654846/134780528-3d47e7c6-a829-4cee-979a-8bf02b70d2a1.png">

<p>
 <br><br>

[contributors-shield]: https://img.shields.io/github/contributors/deno750/TSP_Optimization.svg?style=for-the-badge



# The Game

First released in 2014 on Github by [Gabriele Cirulli](https://github.com/gabrielecirulli), 2048 is a game where the player has to slide numbers on a 4x4 grid to merge them into bigger numbers. Every time a move is completed, the game add a new number to the grid. The objective is to obtain a cell with a value of 2048 in it, although it is possible to reach a higher score.<br><br>

### Additional rules:
- There are 4 possible moves (directions) the player can choose from: up, down, right, left.
- A move has to make a change in the board in order to be valid (i.e. the grid before and after the move must be different).
- A new number is added to the grid after a move is completed, if the move was valid.
- After a valid move, a '2' is added to the grid with a probability of 90% and a '4' with a probability of 10%.
- The player loses when the are no valid moves left

### State space
Calculating the whole state space for 2048 is not an easy task, in fact the enumeration of states still remains an open problem. In 2017, John Lees-Miller [tried to calculate it using a brute force approach](https://jdlm.info/articles/2017/12/10/counting-states-enumeration-2048.html) and he he managed to compute all the possible states up to the tile 64. It took his respectable computer (OVH HG-120 instance with 32 cores at 3.1GHz and 120GB RAM) more than a month and he could only conclude that the state space is much greater than 1.3 trillion states (≫ 1.3 trillion).


### Actions
The set of actions the player it is defined as A<sub>i</sub> ⊆ M = {up, down, left, right}. Where A<sub>i</sub> is the set of allowed moves a player can choose from when the game is in the state S<sub>i</sub>. For example, in Figure 1 the player can choose between the whole set of moves M = {up, down, left, right}, in this case A<sub>i</sub> = M. In Figure 2, the player can only play 2 actions A<sub>i</sub> = {up, right}.

### State Transitions
In 2048 the transition between states is **stochastic**, meaning that given a state of the game and certain move, the resulting state may be different depending on where the new number is spawned and whether is a '2' or a '4'.
Take as example the following game state:
<br>
<br>
<br>
<p align="center">
 <img src=https://user-images.githubusercontent.com/63654846/134788763-43fb75e8-c1cd-463c-8877-5bbd6211063c.png>
</p>

<br>
<br>
 
 Say that the player chooses the move 'left', the resulting possible game states G<sub>i</sub> after the move are 28, because there are 14 empty spots where the new number can appear and the new number is taken from the set N = {2, 4}.

<br>
<br>
<p align="center">
<img width="70%"src=https://user-images.githubusercontent.com/63654846/134788628-bcb44aa4-18b5-4279-a5bc-afeb4f0d01bb.png>
</p>
<br>
<br>

### Score
In the original game, the score starts from 0 and everytime a player adds up 2 numbers the sum of the 2 numbers is added to the score.
For example, merging together two tiles of '2' would increase the score by +4, merging together two tiles of '16' would increase the score by +32.<br>
However, in this version of the game the score of a state of the game S<sub>i</sub> is given by summing up the values of all the tabs. (see examples below)

<br>
<br>
<p align="center">
<img width="40%"src=https://user-images.githubusercontent.com/63654846/134788874-b701f76c-8ea7-4fc6-ac97-6ad13b86b31d.png>
</p>
<br>
<br>

 
## Random walk
A random walk is a random process made of a sequence of random steps. In 2048, the evolution of the score follows a random walk. If there is at least one valid move (i.e. it is not game over), the score of the State S<sub>i+1</sub> is given by the score of the previous State S<sub>i</sub> +2 with a probability of 0.9 and +4 with a probability of 0.1. If it is game over, the score will remain the same.

<br>
<br>
<!-- latex formula: \begin{equation*} S_{i+1} = f(M_i,\ S_i)= \begin{cases} s_i + 2 &\ p = 0.9 &\ if M_i \ne \emptyset \\ s_i + 4 &\ p = 0.1 &\ if M_i \ne \emptyset \\ s_i &\ &\ if M_i= \emptyset \end{cases}\end {equation*}-->
<p align="center">
<img width="70%" alt="Screen Shot 2021-09-25 at 6 05 30 PM" src="https://user-images.githubusercontent.com/63654846/134787043-2d32a12b-23ed-4bb8-8ced-a24de4c8904a.png">
</p>

<br>
<br>
 
 
## Monte Carlo

Monte Carlo methods are a category of algorithms that rely on random sampling to approximate a result that cannot be directly calculated. Sampling a large number of scenarios is possible to estimate boundary conditions that are impossible or difficult to define a priori.

For example, [Nicoguaro](https://commons.wikimedia.org/wiki/User:Nicoguaro) used Monte Carlo to estimate the value of π by drawing points uniformly in a quadrant. Then, by calculating the distance of each point from the origin he determined if such point is within the boundary of the circle or not. Finally, he computed the percentage of points within the boundary over the total points, and he multiplied it by 4 to obtain an estimate of π.
<p align="center">
<img width="40%" src="https://user-images.githubusercontent.com/63654846/134781541-7d6ea43c-4ce2-4f20-b2a3-0d3048521c77.gif">
</p>


[image source](https://en.wikipedia.org/wiki/Monte_Carlo_method#/media/File:Pi_30K.gif)



# Combine Random walk and montecarlo MMRW

For each valid move A<sub>i</sub> ⊆ M = {up, down, left, right}, the algorithm will generate n ∈ ℕ simulations, and in each simulation will take make m ∈ A ⊆ M  random moves. Then it will calculate the average for 
<img width="391" alt="Screen Shot 2021-09-25 at 8 59 24 PM" src="https://user-images.githubusercontent.com/63654846/134789595-db7ead6c-9180-46ee-b492-84aa3ad0e6a7.png">

For example, with s<sub>i</sub> = 1000, A<sub>i</sub> = {up, down, left, right}, n = 1000, and m = 16. we got the following distributions.

<img width="1265" alt="Screen Shot 2021-09-25 at 6 28 22 PM" src="https://user-images.githubusercontent.com/63654846/134787410-5e2ebe8d-161d-499c-836a-f5ed5c543486.png">


![final_graph2](https://user-images.githubusercontent.com/63654846/134789571-d73c6058-a63e-4ca8-946b-605fe21afa57.png)


![graphviz](https://user-images.githubusercontent.com/63654846/134789451-58ea229e-364e-4940-84aa-eb7e9e5f54e8.png)




##df

https://en.wikipedia.org/wiki/2048_(video_game)
https://jdlm.info/articles/2017/12/10/counting-states-enumeration-2048.html
https://drive.google.com/drive/u/0/folders/1Xw_4lVkJyrPH8ahrGQwFJ8SbHLubgWm3
