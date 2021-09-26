<br><br>
<p align="center">
<img width="70%" alt="Screen Shot 2021-09-25 at 1 21 14 PM" src="https://user-images.githubusercontent.com/63654846/134780528-3d47e7c6-a829-4cee-979a-8bf02b70d2a1.png">

<p>
 <br><br>

[contributors-shield]: https://img.shields.io/github/contributors/deno750/TSP_Optimization.svg?style=for-the-badge



# The Game

First released in 2014 on Github by [Gabriele Cirulli](https://github.com/gabrielecirulli), 2048 is a game where the player has to slide numbers on a 4x4 grid to merge them into bigger numbers. Every time a move is completed, the game add a new number to the grid. The objective is to obtain a cell with a value of 2048 in it, although it is possible to reach a higher number of 2048.<br><br>


### Additional rules:
- There are 4 possible moves (directions) the player can choose from: up, down, right, left.
- A move has to make a change in the board in order to be valid (i.e. the grid before and after the move must be different).
- A new number is added to the grid after a valid move is completed.
- After a valid move, a new number is inserted to the grid. it is '2' with a probability of 0.9 and a '4' with a probability of 0.1.
- The player loses when the are no valid moves left

### State space
Calculating the whole state space for 2048 is not an easy task, in fact the complete enumeration of states still remains an open problem. In 2017, John Lees-Miller [tried to calculate it using a brute force approach](https://jdlm.info/articles/2017/12/10/counting-states-enumeration-2048.html), and he managed to compute all the possible states up to the tile 64. It took his decent computer (OVH HG-120 instance with 32 cores at 3.1GHz and 120GB RAM) more than a month and he could only conclude that the state space is much greater than 1.3 trillion states (≫ 1.3 trillion).


### Actions
The set of actions is defined as A<sub>i</sub> ⊆ M = {up, down, left, right}. Where A<sub>i</sub> is the set of allowed moves a player can choose from when the game is in the state G<sub>i</sub>. For example, in Figure 1 the player can choose between the whole set of moves M = {up, down, left, right}, in this case A<sub>i</sub> = M. In Figure 2, the player can only play 2 actions A<sub>i</sub> = {up, left}.
 
<br>
<br>
<br>
<p align="center">
 <img width="40%" src=https://user-images.githubusercontent.com/63654846/134789970-1e4ea796-c1ef-4d6f-803a-41e4331f1358.png>
</p>

<br>
<br>

### State Transitions
In 2048 the transition between states is **stochastic**, meaning that given a state of the game and a certain move, there are multiple possible resulting game states, depending on where the new number is spawned and whether is a '2' or a '4'.
Take as example the following game state:
<br>
<br>
<br>
<p align="center">
 <img src=https://user-images.githubusercontent.com/63654846/134788763-43fb75e8-c1cd-463c-8877-5bbd6211063c.png>
</p>

<br>
<br>
 
Say that the player chooses the move 'left'. There are 28 possible game states G<sub>i</sub> that can result from the move, because there are 14 empty spots where the new number can appear and the new number is taken from the set N = {2, 4}.

<br>
<br>
<p align="center">
<img width="70%"src=https://user-images.githubusercontent.com/63654846/134788628-bcb44aa4-18b5-4279-a5bc-afeb4f0d01bb.png>
</p>
<br>
<br>

### Score
In the original game, the score starts from 0 and everytime a player merges two tiles, the sum of the 2 numbers is added to the score.
For example, merging together two tiles of '2' would increase the score by 4, merging together two tiles of '16' would increase the score by +\32.<br>
However, in this version of the game the score of a state of the game the score S<sub>i</sub> is given by summing up the values of all the tiles. (see examples below)

<br>
<br>
<p align="center">
<img width="40%"src=https://user-images.githubusercontent.com/63654846/134788874-b701f76c-8ea7-4fc6-ac97-6ad13b86b31d.png>
</p>
<br>
<br>

 
## Random walk
A random walk is a random process made of a sequence of random steps. In 2048, the evolution of the score follows a random walk. If there is at least one valid move (i.e. it is not game over), the score of the State S<sub>i+1</sub> is given by the score of the previous State S<sub>i</sub> +2 with a probability of 0.9 or +4 with a probability of 0.1. If it is game over, the score will remain the same.

<br>
<br>
<!-- latex formula: \begin{equation*} S_{i+1} = f(M_i,\ S_i)= \begin{cases} s_i + 2 &\ p = 0.9 &\ if M_i \ne \emptyset \\ s_i + 4 &\ p = 0.1 &\ if M_i \ne \emptyset \\ s_i &\ &\ if M_i= \emptyset \end{cases}\end {equation*}-->
<p align="center">
<img width="70%" alt="Screen Shot 2021-09-25 at 6 05 30 PM" src="https://user-images.githubusercontent.com/63654846/134787043-2d32a12b-23ed-4bb8-8ced-a24de4c8904a.png">
</p>

<br>
<br>
 
 
## Monte Carlo

Monte Carlo methods are a category of algorithms that rely on random sampling to approximate a result that cannot be directly calculated. Sampling a large number of scenarios makes possible to estimate boundary conditions that are difficult or impossible to define a priori.

For example, [Nicoguaro](https://commons.wikimedia.org/wiki/User:Nicoguaro) used Monte Carlo to estimate the value of π by drawing points uniformly in a quadrant. Then, by calculating the distance of each point from the origin he determined if such point is within the boundary of the circle or not. Finally, he computed the percentage of points within the boundary over the total points, and he multiplied it by 4 to obtain an estimate of π.
<p align="center">
<img width="40%" src="https://user-images.githubusercontent.com/63654846/134781541-7d6ea43c-4ce2-4f20-b2a3-0d3048521c77.gif">
</p>


[image source](https://en.wikipedia.org/wiki/Monte_Carlo_method#/media/File:Pi_30K.gif)



# Markov Chain Monte Carlo (MCMC)

Monte Carlo in 2048 can help us determine what is the best move to make next. Since there is only a maxmimum of 4 moves, we can use Monte Carlo to estimate what it will be the average score of the after m moves, if the player decides to move down in the next step.<br>
So, for each valid move A<sub>i</sub> ⊆ M = {up, down, left, right}, the algorithm will generate n ∈ ℕ simulations, and in each simulation will take make m ∈ A ⊆ M  random moves. Then it will calculate the average for score for each valid move. (See image)


<br>
<br>
<!-- latex formula: \begin{equation*} S_{i+1} = f(M_i,\ S_i)= \begin{cases} s_i + 2 &\ p = 0.9 &\ if M_i \ne \emptyset \\ s_i + 4 &\ p = 0.1 &\ if M_i \ne \emptyset \\ s_i &\ &\ if M_i= \emptyset \end{cases}\end {equation*}-->
<p align="center">
<img width="100%" alt="Screen Shot 2021-09-25 at 6 05 30 PM" src="https://user-images.githubusercontent.com/63654846/134790697-a3197fd2-9ed2-49f3-b9ef-5999180f6655.png">
</p>
<br>
<p align="center">
<img width="40%" alt="Screen Shot 2021-09-25 at 6 05 30 PM" src="https://user-images.githubusercontent.com/63654846/134791021-b1f6ddc2-f825-4327-840d-99c4df4da541.png">
</p>
<br>
<br>

Thanks to the Central Limit Thereom, we know that the average score calculated for each valid move is normally distributed, and its standard deviation decreases as the sample size (number of simulations) increases. In fact, the score does not always follow a normal distribution.
<br>
<br>
Example of a sample distribution that does not follow a normal distribution:

<br>
<p align="center">
<img width="40%" alt="Screen Shot 2021-09-25 at 6 05 30 PM" src="https://user-images.githubusercontent.com/63654846/134789595-db7ead6c-9180-46ee-b492-84aa3ad0e6a7.png">
</p>
<br>
<br>

## Comparing sample distributions

Increasing the number of samples will increase the confidence of the model's decision. The picture below shows the difference in the sample distribution when increasing the sample size from n=100 to n=10000. (with s = 1000, A = {up, down, left, right}, and m = 16)
<br>
<br>

<img width="1265" alt="Screen Shot 2021-09-25 at 6 28 22 PM" src="https://user-images.githubusercontent.com/63654846/134787410-5e2ebe8d-161d-499c-836a-f5ed5c543486.png">

![final_graph2](https://user-images.githubusercontent.com/63654846/134789571-d73c6058-a63e-4ca8-946b-605fe21afa57.png)
<br><br><br><br>

# Final result

Even though, the distribution is quite similar, the confidence of the model would increase a lot when increasing the sample size from 100 to 10000.
Here there are two simulations, one made with n=100 and the other with n=1024.<br><br>

n = 100 | n = 1024
:-: | :-:
<video src='https://user-images.githubusercontent.com/63654846/134791782-9da0837b-4b8c-4947-bed7-102c85326eb7.mov' width=180/> | <video src='https://user-images.githubusercontent.com/63654846/134791784-f0f447a9-3b70-4c02-9834-fea11628d738.mov' width=180/>

<br>
<br>

## Sources

https://en.wikipedia.org/wiki/2048_(video_game)<br>
https://jdlm.info/articles/2017/12/10/counting-states-enumeration-2048.html<br>
