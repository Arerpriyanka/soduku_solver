
#### Abstract
Sudoku is a game in which pen, paper and brain usually work together. When you want to give your pen and brain some rest, 
it can be solved with sudoku solvers. Here we will try to make such a Sudoku Solar.
This article aims to take advantage of linear programming concepts to solve sudoku puzzles. We will start by updating some basic
theories behind liner programming and then implement it in Python using PULP package.
Here we will try to solve two types of sudoku puzzles, regular sudoku and diagonal sudoku, with additional rules on sudoku grid diagonal. More on that as we progress.


###### Steps to solve the Sudoku puzzle in Python

Sudoku is a puzzle based on a small number of very simple principles:

* There must be a number in each square.
* Only numbers from 1 to 9 can be used.
* Each 3 × 3 box can contain only 1 to 9 numbers once.
* Each vertical column can contain 1 to 9 numbers only once.
* Each horizontal row can contain 1 to 9 numbers only once.
* Once the puzzle is solved, this means that every number from 1 to 9 in each row, column, and 3 × 3 box will be exactly once.

* In other words, no number can be repeated in any 3 × 3 box, row, or column.
* In this way of solving the Sudoku puzzle, we first assign the size variable M (M * M) of the 2D matrix.
* Then we assign a utility function (puzzle) to print the grid.
* It will assign a number to the queue and call later.
* If we find the same number in the same row or in the same column or in a specific 3 * 3 matrix then 'wrong' will be returned.
* We will then check if we have reached the 8th row and the 9th column and come back correctly to prevent further retreat.
* Then we will check if the value of the column becomes 9 then we go to the next row and column.
* Further we see that if the value of the current position of the grid is greater than 0, we repeat for the next column.
* After checking if this is a safe place, we go to the next column and then assign numbers to the current (row, call) position of the grid. Later we examine the next possibility with the next column.
* As our assumption was wrong, we reject the assigned number and then we move on to the next assumption with the value of the different number.

--------------------------------------------------------

----------------------------------------------------------
##   4W's & 1H
| Sl.No | Questions | Description | 
| :-----: | :-----: | ----- |
| 1. | What | Sudoku is a game in which pen, paper and brain usually work together. |
| 2. | Who | Sudoku solver anyone can play brain sharpening game . | 
| 3. | When | Sudoko gamer can play at free time . |
| 4. | Where | we will try to solve two types of sudoku puzzles, regular sudoku and diagonal sudoku . | 
| 5. | How | In the Sudoku puzzle we need to fill in every empty box with an integer between 1 and 9 in such a way that every number from 1 up to 9 appears once in every row. |
-------------------------------------------------------

![Simple-Matrix-SWOT-Template_Nov2020 (1)](https://user-images.githubusercontent.com/98829237/161314739-83922359-9885-4faf-8d4c-913106ec2a9e.jpg)


---------------------------------------------------------


##  Requirements:
##  High Level Requirements ##
|ID| Description|
| :-------: |----------------------------------------------------------------------------------------------------------------------------------|
| HLR_1 | It shall not have the same number in the same row .                                 |
| HLR_2 | It shall not have the same number in the same column.                             |
| HLR_3 | It shall not have the same number in the same square.  |
| HLR_4 | It shall have numbers from 1-9   |
---------------------------------




## LOW LEVEL REQUIREMENTS:- ##
| HLR_ID |LLR_ID | Design_consideration | 
| :-----: | :-----: | -------------------- | 
| HLR_1 | LLR_1.1 | It shall not have the same number in the same row |
| | LLR_1.2 | it shows wheater it have in same row or not |  
| HLR_2 | LLR_2.1 | It shall not have the same number in the same column |
| | LLR_2.2 | it shows wheater it have in same coloumn or not | 
| HLR_3 | LLR_3.1 | It shall not have the same number in the same square. |
| | LLR_3.2 | it shows wheater it have in same square or not  |  
| HLR_4 | LLR_4.1 | It shall have numbers from 1-9|
| | LLR_4.2 | it show only numbers between 1 to 9 |  
