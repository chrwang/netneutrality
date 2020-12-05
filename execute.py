import list_utilities
import subprocess
import socket
from urllib.parse import urlparse

def get_hostname(raw_url):
    parsed_url = urlparse("http://" + raw_url.split("://")[-1])
    # strip leading www.
    hostname = parsed_url.netloc
    prefix = "www."
    return hostname[len(prefix):] if hostname.startswith(prefix) else hostname

def disclaimer_listener():
    """
    Processes user input to the disclaimer.
    Arguments:
        None.
    Return:
        bool no_quit: Whether the user agreed to thd disclaimer.
    """
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
    """
    Provide a REPL for managing the site list.
    Arguments:
        None.
    Return:
        None.
    """
    no_quit = True
    msg = "Please enter what you would like to do. Enter HELP for a list of commands.\n"
    err_msg = "Please enter a valid command.\n"

    while no_quit:
        cmd = str(input(msg)).lower().strip()
        if cmd == "help":
            # print out a list of commands
            print("\n" + list_utilities.view_help())
        elif cmd == "block":
            # add to block list
            target = input("Enter the url of the site to block: ")
            hostname = get_hostname(target)
            list_utilities.add_to_block(hostname)
            print("Added " + target + " to blocked sites.\n")
        elif cmd == "redirect":
            # add to redirect list
            # and where to redirect to
            target = input("Enter the url of the site to redirect: ")
            dest = input("Enter the url of the redirect destination: ")
            target_hostname = get_hostname(target)
            dest_hostname = get_hostname(dest)
            try:
                dest_ip = socket.gethostbyname(dest_hostname)
                list_utilities.add_to_redirect(target_hostname, dest_ip)
                print("Added {} to redirected sites. It will be redirected to {}\n".format(target_hostname, dest_ip))
            except socket.error:
                print("Redirect url is invalid.")

        elif cmd == "throttle":
            # add to throttle list
            # and throttle delay
            target = input("Enter the url of the site to throttle: ")
            hostname = get_hostname(target)

            delay = ''
            while delay is not int:
                try:
                    dmsg = "Enter the amount of delay time in ms (integer value): "
                    delay = int(input(dmsg))
                    break
                except ValueError:
                    print("Please enter a valid number. ")
            list_utilities.add_to_throttle(target, delay)
            print("Added {} to throttled sites with a delay time of {} ms.\n".format(hostname, delay))
        elif cmd == "viewblock":
            # view list of blocked sites
            site_target = list_utilities.view_block()
            if len(site_target) == 0:
                print("\nNo currently blocked site.\n")
            else:
                print("\nBlocked sites: ")
                print("\n".join(site_target) + "\n")
        elif cmd == "viewredirect":
            # view list of redirected sites
            # and where they redirect to
            site_target, site_dest = list_utilities.view_redirect()
            if len(site_target) == 0:
                print("\nNo currently redirected site.\n")
            else:
                fmt = '{:<50}{}'
                print(fmt.format('Redirected Sites', 'Destination'))
                for t, d in zip(site_target, site_dest):
                    print(fmt.format(t, d))
        elif cmd == "viewthrottle":
            # view list of throttled sites
            # and their delay times
            site_target, site_delay = list_utilities.view_throttle()
            if len(site_target) == 0:
                print("\nNo currently throttled site.\n")
            else:
                fmt = '{:<50}{}'
                print(fmt.format('Throttled Sites', 'Delay Time'))
                for t, d in zip(site_target, site_delay):
                    print(fmt.format(t, d))
        elif cmd == "del":
            # delete given site from block list
            target = input("Enter the url of the site to un-process: ")
            list_utilities.delete_from_list(target)
            print("Deleted " + target + " from all lists.\n")
        elif cmd == "done":
            # end the loop because user is finished editing the lists
            no_quit = False
            print("Running DNS processor...")
        else:
            print(err_msg)

def main():
    if disclaimer_listener():
        # throttle
        list_listener()
        subprocess.run(["sudo", "python3", "dns.py", "dns_list", "-v"])
    else:
        print("Quitting program.")

if __name__ == "__main__":
    main()
