from robotics import Robot

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

def main(): 
    robot = Robot("Quandrinaut")
    robot.say_hello()
    robot.get_scientists_info(SCIENTISTS)
    robot.print_scientists_info()
    robot.accept_search_commands()
    robot.say_goodbye()

if __name__ == "__main__":
    main()
