import subprocess

def disclaimer_listener():
    disclaimer_txt = open("disclaimer.txt")
    disclaimer = disclaimer_txt.read()
    disclaimer_txt.close()
    print(str(disclaimer))

    no_quit = True

    while no_quit:
        inpt = str(input())
        if inpt.lower() == "yes":
            break
        elif inpt.lower() == "no":
            no_quit = False
            break
        else:
            print("Please enter YES or NO.")
    
    return no_quit

def list_listener():
    no_quit = True
    msg = "Please enter what you would like to do. Enter HELP for a list of commands.\n"
    err_msg = "Please enter a valid command.\n"

    while no_quit:
        cmd = str(input(msg)).lower()
        if cmd == "block":
            # add to block list
            print("temp")
        elif cmd == "redirect":
            # add to redirect list
            # and where to redirect to
            print("temp")
        elif cmd == "throttle":
            # add to throttle list
            # and throttle delay
            print("temp")
        elif cmd == "viewblock":
            # view list of blocked sites
            print("temp")
        elif cmd == "viewredirect":
            # view list of redirected sites
            # and where they redirect to
            print("temp")
        elif cmd == "viewthrottle":
            # view list of throttled sites
            # and their delay times
            print("temp")
        elif cmd == "delblock":
            # delete given site from block list
            print("temp")
        elif cmd == "delredirect":
            # delete given site from redirect list
            print("temp")
        elif cmd == "delthrottle":
            # delete given site from throttle list
            print("temp")
        elif cmd == "done":
            # end the loop because user is finished editing the lists
            no_quit = False
        else:
            print(err_msg)

def main():
    if disclaimer_listener():
        # throttle
        list_listener()
        subprocess.run(["sudo", "./run_dns.sh"])
    else:
        print("Quitting program.")

if __name__ == "__main__":
    main()
