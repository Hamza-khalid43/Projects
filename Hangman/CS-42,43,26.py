def hangman():
    """define the whole game and a global function for all the functions"""
    import random
    admin_user="abc"    #the user name for the admin
    admin_pass="123"    #the pass word for the admin


    def choice():
        """takes an input from the user and work on the respective option"""
        alert_check = False
        while alert_check == False:    #to ask in loop if entered wrong choice
            choice = int(input("""Enter your Choice
    1.User
    2.Admin  """))

            if choice == 1:
                user()
                alert_check = True
            elif choice == 2:
                admin()
                alert_check = True
            else:
                print("------------------Enter Valid option-------------------")

    def player_score(word, guess, username):
        """print and save the score achieved by the user"""
        score = guess * len(set(word))    #using the formula for score
        file1 = open("highscore.txt", "a")
        file1.write(f"{username}={str(score)},")    #writing the scores on a file to obtain highscores
        file1.close()
        print("Your score is", score)   #prints the score
        highscore(score)


    def highscore(score):
        """prints the highest score among the players with name"""
        file1 = open("highscore.txt", "a+")       #opening the file where  scores are save
        file1.seek(0)  # --> Incase if the file already exist then it will take the pointer to the start.
        read = file1.read().split(",")
        read.remove("")
        player_highscore = 0
        highscorer_name = ""
        for i in read:
            if "=" in i[-2:]:
                if player_highscore < int(i[-1:]):
                    highscorer_name = i[:-2]
                    player_highscore = int(i[-1:])
            else:
                if player_highscore < int(i[-2:]):
                    highscorer_name = i[:-3]
                    player_highscore = int(i[-2:])
        while_checker2=False
        while while_checker2 == False:
            highscore_panel=int(input("""enter your choice
    1.See the high scorer
    2.Play again 
    3.Open as an admin  """))
            if highscore_panel == 1:
                print(f"{highscorer_name} is the best player with a score of {player_highscore}")
                print("________________________________________________________________________")
                print("you are finished with game!!!!!")
                while_checker2 = True
                ask=int(input("""enter a choice
    1.want to play again
    2.finish  """))
                if ask == 1:
                    user()                   #enters in the game again
                elif ask == 2:
                    print("THANKS FOR PLAYING")

            elif highscore_panel == 2:
                user()                         #enters in the game again
                while_checker2 = True
            elif highscore_panel == 3:
                admin()                        #enters in the admin panel
                while_checker2 = True

            else:
                print("invalid choice")


    def user():
        """have the whole game in it including extraction of words from the file
        winning commands and logic as well as losing command and logics"""
        name=input("enter your name")
        print(f"hey {name} welcome to hang man game \nYou have 6 turns and 3 warning to guess")

        words_file=open("words.txt","r+")
        for i in words_file:
            words_list=i.split(" ")
        word=random.choice(words_list)     #picks a random word from the list
        print(word)
        turns = 6
        guessmade=''
        valid_entry="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" #all the valid entries
        vowels='AEIOUaeiou' #to identify that whether the wrong guessed character is a vowel
        consonants='bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSVWXYZ'  #to identify that whether the wrong guessed character is a consonant
        warning=3
        guessable_list=[chr(i) for i in range(97,123)]    #for printing available letters above every guess
        guessable_str=" ".join(guessable_list)
        print("guess the words that is", len(word), "long")


        while len(word) > 0:
            main_word = ""

            for letter in word:
                if letter in guessmade:
                    main_word = main_word + letter
                else:
                    main_word = main_word + "_"

            if main_word == word:
                print(main_word)
                print("""__________________________
    CONGRATULATIONS YOU WON!""")
                player_score(word, turns, name)           #to print the score the score function is called here
                break

            print("-----------------------------------------------------------------------")
            print("guess the words", main_word)
            print(f"you have {turns} guesses ")
            print("available letters:", guessable_str.upper())
            guess = input("guess the letter").lower()
            if guess in guessable_str:
                guessable_str = guessable_str.replace(guess, "")
            else:
                print("invalid entry")
                print("YOU LOST A WARNING")
                warning -= 1

            if guess in valid_entry:
                guessmade = guessmade + guess
            else:
                print("-----------------------------------------------------------------------")
                print(f"you have {turns} guesses ")
                guess = input("enter a valid character").lower()

            if guess not in word:
                if guess in vowels:
                    vowels = vowels.replace(guess,"")            #so it dont cut turns if same guess is repeated
                    turns = turns - 2

                if guess in consonants:
                    consonants= consonants.replace(guess, "")    #so it dont cut turns if same guess is repeated
                    turns = turns - 1

                if warning == 0 or warning <0:
                    print("-----------------------")
                    print("you are out of warnings")
                    print("YOU LOST A guess")
                    print("-----------------------")
                    turns -= 1

                if turns == 5:
                    print("5 guesses left!!!!")


                elif turns == 4:
                    print("4 guesses left!!!!")

                elif turns == 3:
                    print("3 guesses left!!!!")


                elif turns == 2:
                    print("2 guesses left!!!!")

                elif turns == 1:
                    print("1 guesses left!!!!")

                if turns <= 0:                  #so the guesses dont go in negative
                    print("YOU LOST!!!")
                    print("you are out of guesses")
                    print("^^^^^^^^^^^^^^^^")
                    print("the word was", word)
                    lost_choice=int(input("""enter your choice
        1.play again 
        2.Finish   """))
                    if lost_choice == 1:
                        user()                              #will take you back to the game again
                    elif lost_choice == 2:
                        break


    def admin():
        """have all the admin commands and prevent intruders from accessing it"""
        print("YOU ARE NOW IN THE ADMIN PANEL")
        user_name=input("enter user name:")                      #user name and password for admin is fixed above
        password= input("enter password:")
        if user_name==admin_user and password==admin_pass:
            def admin_panel():
                """have the options for the administrator that what he have to do as an admin """
                admin_work = int(input("""Enter Your Choice
    1.Add a Word
    2.Reset Score
    3.Logout  """))                         #for different works admin can do

                if admin_work == 1:
                    def add_word():
                        """have the commands for 1 work of an admin , to add a word """
                        while_Checker = True
                        while while_Checker == True:

                            words_file = open("words.txt", "r+")
                            words_file.read()
                            added_word = input("enter the word you want to add:")
                            words_file = words_file.write(" " + added_word)     #space is fixed because the split function is used by space in word file
                            print("YOUR WORD IS ADDED")
                            adder = int(input("""Enter Your Choice 
    1. Add a new Word 
    2. Exit  """))

                            if adder == 1:
                                while_Checker = True
                            else:
                                while_Checker = False
                                admin_panel()                      #will take you back to the admin panel
                    add_word()
                elif admin_work == 2:
                    def reset():
                        """have the second option for the admin to reset the scores"""
                        reseter=int(input("""are you sure you want to reset
    1.yes
    2.no  """))
                        if reseter == 1:
                            open("highscore.txt","w").close()           #it will  clear all the things in the file
                            print("high score are resetted")
                            print("you are in the admin panel")
                            admin_panel()                #will take you back to the admin panel
                        if reseter == 2:
                            print("you are in the admin panel")
                            admin_panel()                       #will take you back to the admin panel
                    reset()

                elif admin_work == 3:
                    choice()                                    #will take you back to the choice panel
                else:
                    print("invalid option \n you are in the admin panel")
                    admin_panel()                                #will take you back to the admin panel

            admin_panel()
        else:
            print("intruder \n enter correct user name password")
            admin()                         #will take you back to the admin

    choice()
hangman()















