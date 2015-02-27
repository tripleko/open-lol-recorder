This is a simple python script that allows you to record games on the website op.gg. I made this as an alternative to the closed source or Windows only solutions I found.

Simply write out a list of region codes and summoner names into the summoners.txt file and run the script with python from a console or command line. Every two minutes the script will send a request to record any summoners that are in game on your list.

The summoners.txt file needs to strictly follow a format of

```
regioncode summonername
```

on each line, seperated by a single space. I've included some examples in summoners.txt that you may edit with your own.

Region codes are pretty much the same as the op.gg prefixes and are as follows:

* br - Brazil
* eune - Europe Nordic East
* euw - Europe West
* lan - Latin America North
* las - Latin America South
* na - North America
* oce - Oceanic
* ru - Russia
* tr - Turkey
* kr - Korea

Tested with Python 2.7 under Win7 and Ubuntu. Feel free to let me know if you encounter problems. I initially churned this out in a few hours as something for myself but I figured I may as well share it with the world.
