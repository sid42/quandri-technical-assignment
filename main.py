from robotics import Robot

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

def main(): 
    robot = Robot("Quandrinaut")
    robot.say_hello()
    
    for scientist in SCIENTISTS: 
        result = robot.open_and_parse("https://en.wikipedia.org/wiki/{}".format(scientist.replace(" ", "_")))
        print("Here is some information about", scientist)
        print("Bio: ", result["bio"])
        print("Date of Birth: ", result["birth"])
        print("Date of Death: ", result["death"])
        print("Age: ", result["age"], "\n\n")

    robot.say_goodbye()


if __name__ == "__main__":
    main()
