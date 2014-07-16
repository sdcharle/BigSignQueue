#This is code for the Scrolling LED Alpha 320C sign at Bloominglabs.

##It includes:
* A SQLite Database where messages are stored
* A twisted server listening on port 6666 for JSON-formatted messages to put on the queue
* A script to pull events from the Bloominglabs Calendar and put them in the Queue (and, ultimately, on the sign)
* An IRC bot (again, Twisted) that will put messages in the channel starting with '!s ' on the sign

##Some notes:
You need these modules
(add here)

You need to setup an account so as to use the Google Calendar API
(references here)

You need an actual sign using the alpha protocol

I hope you like this, also I hope my new cable lasts longer than the previous one did

##The 'API'
You can send JSON to the server on port 6666 (or whatever port you end up using!)
The format is:
```
{
  "start_time":"2014-08-23 12:34:56",
  "life_time":900,
  "priority":3,
  "immediate":"False",
  "message":"Phone's ringing, dude"
}
```

But you could send this:
```
{
  "message":"Phone's ringing, dude"
}
```
And the message would have a lifetime of the default (60 seconds currently but I'm thinking that won't work if you have a lot in your queue.)

SDC
http://bloominglabs.org
