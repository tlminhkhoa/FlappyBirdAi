# Flappy Bird AI ![Logo](https://github.com/tlminhkhoa/FlappyBirdAi/blob/master/assets/bluebird-midflap.png?raw=true)

###### [![Run on Repl.it](https://repl.it/badge/github/tlminhkhoa/FlappyBirdAi)](https://repl.it/github/tlminhkhoa/FlappyBirdAi)


> A NEAT inspired algorithm playing Flappy Bird. 



<p style="text-align: center">
    <img 
    width=""
    height="300"
    src="https://github.com/tlminhkhoa/FlappyBirdAi/blob/master/assets/background-day.png?raw=true"
  ></p>

![permalink setting demo](https://i.imgur.com/PjUhQBB.gif)
- Table of Content
[ToC]

---



## Demo

- Demo on local computer

{%youtube PJuNmlE74BQ %}

## Result Analysis 

## Installation

Clone the project

```bash
  git clone https://github.com/tlminhkhoa/FlappyBirdAi
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install requirements.txt 
```

Run the game

```bash
  python FlappyBirdTrain_Crossover.py
```



## :memo: How it work

### The Neural Network

This is the controlling unit of each bird, the deciding factor in the game. Each brain is created through my implementation of fully connected NN, the file call NN.py can be found on the Github link.

The following is the default parameter for each bird:
* 5 number of input
* 2 number of output ( jump or not to jump)
* 1 hidden layer
* 6 nodes in each hidden layer
* Tanh activation function

Each of these parameters can be changed through the input variable.


 <p style="text-align: center">
    <img 
    width="750"
    height=""
    src="https://github.com/tlminhkhoa/FlappyBirdAi/blob/master/assets%20ReadMe/NN.PNG?raw=true"
  ></p>
 
 
:rocket:

 The bird vision contains 5 views (input):
 
 <p style="text-align: center">
    <img 
    width=""
    height=""
    src="https://i.imgur.com/hTdUt7c.png"
  ></p>
  
 <p style="text-align: center">
    <img 
    width=""
    height=""
    src=https://i.imgur.com/q5srtja.png)>
</p>

Each of these inputs is normalized the game parameter before being passed to the Neural Network.



### The Neat-inspired algorithm
#### Fitness function

Fitness is a way to measure how long a bird can survive through the environment, calculated using the clock on the game. Each given generation contains a flock of 100 birds, the 10 top bird is selected base on their fitness to carry on to the next generation. These top 10 birds will be called 10 types.

#### Mutation process

Mutation is the ability of the bird to change its genetic by itself through generations, mimicking the real-world mutation caused by radiation and other factors.

This is achievable by randomly (mutation rate) modify the weight of each bird by a small margin (mutation margin).

 <p style="text-align: center">
    <img 
    width="400"
    height=""
    src=https://i.imgur.com/BrUpw50.png
>
</p>

A loop is created to go through each bird weight matrix. At each weight, a random variable is generated to decide the weight should mutate or not. The action will be taken if the mentioned variable is smaller than 0.3. 



 <p style="text-align: center">
    <img 
    width=""
    height=""
    src=https://i.imgur.com/0chatsx.png
>
</p>

#### Cross-Over process

Cross-over is a method for the top birds to combine their genetic to produce offspring, that potentially be better than the parents. My home-made cross-over algorithm contains 3 main components :
* Replication
* Pairing
* Cross-swap

With the combination of the three steps, hopefully, the algorithm successfully mimics the heredity process of nature.

##### Replication 

From each round, the top 10 birds with the highest fitness are selected. Each bird will be replicated 10 times using deep copy. This produces a new flock of 100, 10 of each type of bird.


<p style="text-align: center">
    <img 
    width=""
    height=""
    src=https://i.imgur.com/WS1HcJh.png
>
</p>


##### Pairing

Now since we have a new flock of 100 birds, 10 of each, the next task is to pair them with each other to create “families”. The method is simple, but a bit hard to explain.


<p style="text-align: center">
    <img 
    width=""
    height=""
    src=https://i.imgur.com/EF5GVW2.png
>
</p>

The second step boiled down to the problem of generating unique 45 pairs from 90 birds. We can view the flock of birds as a 9x9 matrix. The algorithm simply pairs the n row with the (n+1) column.

<p style="text-align: center">
    <img 
    width=""
    height=""
    src=https://i.imgur.com/PjjubwE.png
>
</p>

##### Cross-Swap

Cross-swap provides a way for a pair of birds to exchange information. It archives this by randomly swapping the neurons of two birds.

Again the weights of 2 neural networks can be view as 2 matrixes. There is a 40% chance (swap rate) that an individual weight from the first matrix will be swapped the weight in the same coordinate from the second matrix.


<p style="text-align: center">
    <img 
    width=""
    height=""
    src=https://i.imgur.com/mQ2173j.png
>
</p>


### The Game

This is my first homemade game, fortunately, tutorials are abundant for this intro program on the internet, one of the reasons I choose this game to dive into the genetic algorithm.

The Clear Code youtube channel has a great tutorial on this. Following his instruction and assets, I was able to make a replica within a day.

{%youtube UZg49z76cLw %}


Sorry if my code is a bit messy for anyone looking through them :( .


Here is some of the adjustable variable to balance the game difficulty:
* The distance from the above and below the pipe 
* The time interval between two spawning pairs of pipes.
* The gravitational force on the birds.
* The jumping force of the birds.


With these parameters, we can test out the limitation of our learning algorithm with different difficulties.


## Acknowledgements

 - [Clearcode FlappyBird](https://github.com/clear-code-projects/FlappyBird_Python)
 - [Code Bullet FlappyBird A.I](https://www.youtube.com/watch?v=WSW-5m8lRMs&ab_channel=CodeBullet)
