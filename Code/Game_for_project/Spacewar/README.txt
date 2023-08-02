1. Install pygame in the command prompt or terminal: python3 -m pip install -U pygame --user
	
2. The image might not load due the change of the directory. If you see the error related to image, copy and paste the path of the image from the folder. For image ship.bmp, replace the path and paste it in ship.py in the line self.image = pygame.image.load(). For image alien.bmp, replace the path and paste it in alien.py in the line self.image = pygame.image.load(). 

3. To play the game run python3 spacewar.py in terminal or command line, press directional key left to move to the left, press directional key right to move to the left, press space bar to shoot the bullets and press Q to end the game. 

4. spacewar.py is the main code for running the game. Run the program with python3 spacewar.py

5. game_functions.py have all the functionality for running the game. This file is imported to the main code. This codes has event that occur during the game. It has events for directional keys and mouse, play button, bullets, aliens fleet, conditions for ship collision and outcome when the ship collide at the bottom. 

6. settings.py has the class for settings to run the game. It has dimension and color for both bullets and screen. It also has speed settings for the speed ships and bullets. 

7. ship.py is the class creating the ship's position, movement and speed.

8. alien.py has class for the alien forces. It also has ships position, movement and speed.

9. bullet.py has the bullet class which stores the bullets. The feature of this class are its position, color, speed and dimensions. 

10. gamestats.py is the class for tracking the statistics for the game. It contributes the current statistics and check if the game need to reset. 

11. button.py has the class to create the play button in the screen. The functionality of this class is to draw the play button with its color, dimension, position, color, and fonts. 

12. score.py has the class for recording the score whenever the bullets hits the alien ship. The functionality includes updating the screen, color, fonts, calculating the score and showing the score. 

13. Importing sys lets us have access system specific parameters and functions.It helps to exit the game when the player quit the game. 

14. Import pygame gives us the collection of different modules in a single python package. 

15. From pygame.sprite import sprite, it can group all the related elements in the game and act as one. 

16. From pygame.sprite import group, it gives the simple base class for visible game objects.

17. From time import sleep, it pauses the gave when the ship hits the aliens ship. It imports the time functionality form the python library. 

18. Import pygame.font writes the text to the screen. 