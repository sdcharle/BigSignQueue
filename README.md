#This is code for the Scrolling LED Alpha 320C sign at Bloominglabs.

##It includes:
 *A SQLite Database where messages are stored
 *A twisted server listening on port 6666 for JSON-formatted messages to put on the queue
 *A script to pull events from the Bloominglabs Calendar and put them in the Queue (and, ultimately, on the sign)
 *An IRC bot (again, Twisted) that will put messages in the channel starting with '!s ' on the sign

#Some notes:
You need these modules
(add here)

You need to setup an account so as to use the Google Calendar API
(references here)

You need an actual sign using the alpha protocol

I hope you like this, also I hope my new cable lasts longer than the previous one did

SDC
http://bloominglabs.org
