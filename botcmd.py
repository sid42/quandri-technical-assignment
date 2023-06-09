import cmd

class BotCmd(cmd.Cmd):
    intro = "Now that we have all the information about the scientists, we can look up scientists by their relevant information, like Google search. \nTry doing \"search English\" to see all English scientists. Use help or ? to see all commands."
    prompt = "(bot) "
    
    def __init__(self, search_func, add_func): 
        super().__init__()
        self.search_func = search_func
        self.add_func = add_func

    def do_search(self, arg):
        """search <text> (eg. search einstein)"""
        result = self.search_func(arg)
        if len(result) != 0: 
            print("You might be looking for the following scientists:")
            for scientist in result: 
                print("Name: ", scientist["name"])
                print("Bio: ", scientist["bio"])
                print("Date of Birth: ", scientist["birth"])
                print("Date of Death: ", scientist["death"])
                print("Age: ", scientist["age"], "\n\n")
        else: 
            print("Hmm looks like I could not find the scientist you were looking for...")

        print("Continue searching using search or type quit to exit")

    def do_add(self, arg): 
        """add <scientist_name> (eg. add Nikola Tesla)"""
        self.add_func([arg])
        print("Added information for", arg)
    
    def do_quit(self, arg):
        """Quit the command interpreter"""
        print("Quitting...")
        return True