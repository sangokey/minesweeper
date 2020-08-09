# Minesweeper by Sang Ok Suh


## Contents  
I have provided one file and one image folder:  

1. minesweeper.py  
2. images  

Both files have to be in the same folder to run the pygame successfully.  
*Program Instructions Available in the bottom*   


## Overview  
I have recreated the famous Minesweeper game with two modes and two difficuties:  

**Modes**:   
1. **Normal** - Normal Minesweeper Game: Goal is to uncover all safe cells (cells without bombs).   
2. **Flags** - Guess the bomb locations: After the user guesses all the bombs (shown in top left), the game will check if the guesses (flags) are correct.   
*In the flags mode, the user can guess the bomb at any time in the game.*   

**Difficulty**:  
1. **Easy** (9x9 with 10 bombs)  
![](images/easy.JPG)
2. **Hard** (16x16 with 40 Bombs)  
![](images/hard.JPG)



## Game Description  
In Minesweeper, all cells are initially hidden.  
Clicking on a cell reveals its contents.  
If the cell contains a mine, then the game ends and the player loses.  
If the cell does not contain a mine, the number of adjacent cells with bombs is revealed.  
If a cell does not contain a mine, and it is not next to a mine, a blank cell is displayed and other adjacent black cells are revealed.  
The game ends when, either a mine is uncovered (loss) or all cells are revealed that do not contain a mine (win).  
First click cannot be a mine. If first click is a mine, game is restarted.  


## Game Instructions  
1. First click cannot be a mine, if it is then the game restarts automatically.
2. From the main page, click on a difficulty level.  
3. Top left shows the the number of bombs left to find.  
4. Top right shows the time counter.  
5. The middle shows the status of the game: thumbs up for on-going game, thumbs down for lose, crown for win.
6. You can click the middle icon to restart the game within the same difficulty.  
7. You can navigate to the main menu (to choose another difficulty) or quit the game using the buttons on the bottom.  

## Algorithm Description
1. **Normal Mode**:  
Every time an user makes a move (not a mine), this program loops through the board to check for winning conditions.  
The winning condition is: when there are no empty spaces left and no flags in empty positions.  
The loop through the board takes O(m\*n) time.  
The number of maximum moves a user can take is m\*n times because there are maximum m\*n possible cells.  
Therefore, the complexity of the algorithm that verifies the solution is **O(m<sup>2</sup>n<sup>2</sup>)**.  

2. **Flags Mode**:  
When there are no remaining guesses left (10 for easy, 40 for hard), the program will loop through the board (mxn) to find all the flags (guesses): m\*n.  
For each flag location, all adjacent cells are found (8): 8\*m\*n.  
For each adjacent cells, the number of adjacent cells (max 8) with bombs and the number of adjacent cells with flags (guesses) are found: 8\*8\*m\*n.
If the number of bombs and the number of flags do not match, user loses the game.  
Otherwise, guesses are correct and user wins.    
The algorithm complexity is **O(m\*n)**.  

## Program Instructions  
To run the game in the terminal, you need to install **pygame** if you don't have it installed.  

**From the pygame.org website:**    
The best way to install pygame is with the pip tool (which is what python uses to install packages).   
Note, this comes with python in recent versions.   
We use the --user flag to tell it to install into the home directory, rather than globally.  

	python3 -m pip install -U pygame --user  
	

After intalling pygame, you can open the game in the terminal using the following scripts (depends on your python):  
	
	py minesweeper.py  
	
	python3 minesweeper.py  
