# spaghetti-bot
Using discord.py I think I've made a nifty bot. The extensions to this library have also allowed me to make it fully modular - follow the example in the existing module file (Colors.py) to make your own modules.

# Dependancies
Requires discord.py, Python >= 3.6.
# 'Installation'
You will need to create a Discord bot account and supply your key (not your client ID or secret) in key.txt. This file should be placed in the same directory as main.py. There are many guides to doing this on the internet.
Again refer to the Internet, this time for how to add your new bot to your server. Run the script and if you did everything right, the bot will come online and respond to commands. The bot must be given at least the Manage Roles permission, and its role must be placed quite high to avoid permission errors. Overall, I would recommend that you just give it administrator privileges to avoid issues like this; you can see the source code and you know it's not doing anything harmful nor does it auto-update.
# Usage
In this repo, the command prefix is '$' and the only command is '$color' or its alias '$colour'. This takes one argument, a single 6-digit (RRGGBB) hex colour code (hash or not doesn't matter) and changes your name in the Discord server to the specified colour.

Example usage: `$colour #ff0000` changes your name to be red.

# License

Copyright 2017 jay0@me.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
