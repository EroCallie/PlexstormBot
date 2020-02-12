# PlexstormBot
Extensible Python Plexstorm Bot for Automated Interaction with Chat and Site Events

The code here is what you will need in order to get started with a basic Plexstorm Bot. You will need Python 3.6 or 
higher installed on your system to make use of this project!

#### Python Module Dependencies:
- websockets

Dependencies can be installed by running

\>$`python -m pip install <modulename>`


## Getting Started
Before you can launch the bot, you will need to copy the `config.template.ini` file to `config.ini` and edit it with 
your login information for your streamer and bot accounts. You may use the same information for both.  Bot login is used
 for any messages sent to or received in chat. Streamer login is used to capture site events and setup stream 
information when using the relevant functions in a script from PlexLib. the `[Channels]` section can be configured to 
join as few or as many channels as you would like with your bot account, in case you intend to provide a service to 
several channels. Remember to include your own channel for chat integration to work!

By default, this bot will do nothing as-is. Only by filling the `scripts` folder with user scripts will any real 
functionality beyond simply logging in be provided. More repositories will be provided on this github account with 
functional scripts both to help you get started with helpful features and to study how best to make your own scripts, 
but the basic formula is to create a subfolder of any name inside `scripts/` and create a file called `main.py` that 
will function as the initialization for your script.  You will want to `#import PlexLib` from your script in order to 
gain access to the features most useful for interacting with the PlexStorm website.  Generally speaking, the `retrieve_`
functions  are intended to be used by PlexBot and should not be used by scripts without understanding the implications 
of doing so by studying the PlexBot code. 

In order to avoid name clashes in functions between scripts, you will want to use a class to contain any functions you 
intend to register as a callback with PlexLib in order to gain access to helpful events, such as `on_message` which 
provides the script with a plethora of information about the channel and message details each time a chat message is 
received in a channel that is within the configuration file.  Make sure any functions you intend to register as 
callbacks are designated as static methods unless you are certain you understand how the script loading works within 
PlexBot. Check within PlexLib for details of what all callbacks are available, but note that most of the functionality 
you are most likely to want is provided by the `on_message` callback, including tips and subscription details. There is 
currently no way within Plexstorm to track follower counts beyond watching the total by polling periodically, and this 
action will not be able to provide usernames for new followers, nor differentiate a new follower from someone who 
rapidly toggles following on and off, so take care when implementing alerts involving follower counts. 

I hope creating your own scripts to use with the bot proves to be easy and fun!    

## License Details

This python contents repository are licensed under the GNU AGPLv3. Any scripts created for use with the bot are NOT
subject to this licence, and may be licenced in any way desirable to the author, as long as they respect any other 
copyrights that are applicable to their use of libraries. 

_The AGPL differs from the standard GPL in that modifying the source code and then providing a network service that uses 
that code (even if not distributing the software) triggers the copyleft provisions of the license, and source code must 
be made available upon request to anyone who is capable of using the service. This license is only applicable to PlexBot
 and PlexLib, so that any research done to extend the capabilities of the core bot itself and its ability to interact 
with the Plexstorm website will be of maximum usefulness to the entire community._ 

TL;DR

**How you use the callbacks and functions already provided by the bot is entirely up to you and does not require 
releasing any of your personal script code!  I only ask that you share core site interaction details, most of which I 
have already researched and provided within PlexBot with an interface via PlexLib!** 
