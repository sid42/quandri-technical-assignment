from robotics import Robot

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

def main(): 
    robot = Robot("Quandrinaut")
    robot.say_hello()
    print("I am currently indexing information for the given scientists")
    robot.get_scientists_info_from_wiki(SCIENTISTS)
    robot.print_scientists_info()
    robot.accept_search_commands()
    robot.say_goodbye()

if __name__ == "__main__":
    main()
