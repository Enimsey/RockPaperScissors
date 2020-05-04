# HOWTO
There are two ways of testing the code:                                                                                             
1/ With command line by typing:                                                                                           
          a/for playing against the computer: python main.py 1 and follow instructions                                                                                            
          b/for playing against another person: python main.py 2 and follow instructions        

2/ With an interface:                                                                                             
In a first terminal, launch serverui.py and hit "Start"                                                                                            
In a second terminal, launch playerui.py, enter your player name.                                                                                            
      a/ Against Computer mode: Check the radio button with label "1" (for game against computer) and click connect
        You can already start playing by picking rock paper or scissors.                                                                                            
      b/ Against Friend mode: Check the radio button with label "2" (for game against a friend) and click connect
        Your friend needs to do the same (in a new terminal)                                                                                            
        Once your friend is connected two, you can start picking rock, paper or scissors...                                                                                       
                                                                                                    
 To restart a session (to change the game mode, reinitialize the score, the player name, click restart on server and player ui's)
 
 # EXTENDED VERSION
 To test the extended version (command line or ui) with Rock Paper Scissors Lizard Spock, you just need to uncomment lines 9 and 10 and comment lines 5 and 6.
 
 # REQUIREMENTS
 Python >= 3.5 for PyQt5: https://pypi.org/project/PyQt5/
 
