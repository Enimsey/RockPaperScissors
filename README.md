# HOWTO
There are two ways of testing the code:
1/ With command line by typing: 
          for playing against the computer: python main.py your_choice (with your_choice being 0: rock, 1: paper, 2: scissors)
          for playing against another person, in the same terminal: python main.py your_choice your_friends_choice

2/ With an interface:
In a first terminal, launch serverui.py and hit "Start"
In a second terminal, launch playerui.py, enter your player name.
      * Against Computer mode: Check the radio button with label "1" (for game against computer) and click connect
        You can already start playing by picking rock paper or scissors.
      * Against Friend mode: Check the radio button with label "2" (for game against a friend) and click connect
        Your friend needs to do the same (in a new terminal)
        Once your friend is connected two, you can start picking rock, paper or scissors.
        
 To restart a session (to change the game mode, reinitialize the score, the player name, click restart on server and player ui's)
 
 
