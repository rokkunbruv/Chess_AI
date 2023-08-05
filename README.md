# Chess_AI
by rokkunbruv<br>
June 2023 to recent<br>
Version 1.1


My technically second project if we consider my calculator program in C++ that makes use of the terminal as my first project and ignoring my second and third 'projects' which are the unfinished algorithm visualizer and that space invaders knockoff without adding something new to the code respectively. Yeah i know it's going to be terrible considering I dont have that much experience in making personal projects so do me a favor and make the code a lil bit efficient. Arigayto!

Tho i mostly coded the whole thing by following through a tutorial (huge shoutout to [Coding Spot](https://youtu.be/OpL0Gcfn4B4) for the tutorial), I tried my best to make this code my own by adding in features the tutorial failed to cover, such as the undo feature and checkmates and stalemates, you know, as a learning experience to revisit my forgotten knowledge on programming in Python (it's been a while since I've dabbled into Python) and especially OOP.

## Features
- **Player vs player mode**
- **Computer mode** (*can only make random moves*) that you can fight against (you'll probably win most of the time) or have two computers fight each other by pressing `C`
- Can do **castling** and **en passant** (i pray to God they're bugless)
- **Check**, **checkmate**, and **stalemate** feature (draw feature currently being developed)
- You can **switch themes** by pressing `T` (yay colors)
- The **ability to drag pieces** (you do have to drag them when you want to make a move)
- An **undo** feature to fix all your mistakes, like your lif- (i pray to God the second time it'll be bugless)
- The ability to **restart your game** by pressing `R` (whenever you feel like you've messed up the ordering of your variation of Sicilian defense)

## Installation Guide
If you're not the creator of this code and has somehow managed to access this code for some reason, you can refer to the installation guide below to help you install this little game I made to your PC and try this one out.
1. Download this repo (duhh) through clicking the download button (go find it idk u know how github works) or typing this in your terminal *(requires git to work)*
```
git clone https://github.com/rokkunbruv/Chess_AI.git
```
2. Proceed to either Step 2.1 (running the code as is) or Step 2.2 (running the code thru a virtual environment, *HIGHLY RECOMMENDED*)

### Step 2.1
Go run the code by typing 

```
python src2/main.py
```

Ensure that you have the Python interpreter and PyGame module installed

### Step 2.2
In running the code through a virtual environment (venv), go make one by typing

```
python -m venv nameOfVenv
```

Next update Pip and install PyGame. Then, activate the venv by typing (for WIndows Powershell)

```
venv/Scripts/Activate.ps1
```

 or (for Bash) i think

 ```
 source venv/bin/activate
 ```

 Then you can execute the code by typing

 ```
 python src2/main.py
 ```

 If you want to exit the venv, you can type

 ```
 deactivate
 ```
 
 The reason why I highly recommend this is that you may encounter a trouble when installing PyGame because there might be other packages installed in your system that may conflict with PyGame. If this doesn't occur to you, then good for you! But I still recommend this because PyGame might get into conflict with your other packages you're gonna install in the future, which will just provide you with more pain, so I'm doing you a favor by creating a venv instead.


## What's New in v1.1?
- Only the code. Code looked too messy imo (which is probably the reason why my v1.0 code had a lot of bugs) so I made it cleaner and organized everything to wear it is should.
- Perhaps the major improvement of my code is moving all of my move calculation logic to my *Pieces* class. This is because my *Board* class got too long and I prefer my move calculation logic to be done by my pieces themselves, not the board.