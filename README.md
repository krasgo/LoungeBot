# LoungeBot
A Discord bot I'm making for some spectacular friends. <br>
(update: a cat is now a collaborator on this bot)
- - - -
## Features
* **`/imgur <count>`**: Generate \<count\> random imgur links and display them, up to 5.
  * Example: `/imgur 5`: will make the bot message the channel 5 imgur links.

* **`/survey <action> <message>`**: Create anonymous surveys with anonymous answers.
  * `/survey prompt Is HTML a programming language?`: to start a survey.
  * `/survey respond Yeah it is!`: to respond to a survey.
  * `/survey end`: to end a survey (if you started it) and show the results.

* **`/translate <message>`**: Translate <message> to English, assuming \<message\> is not in English.

* **`/translatemix <count> <message>`**: Translate \<message\> through a chain of \<count\> different languages, then end with an English translation. \<message\> can be in any language.
  * `/translatemix 3 Lorem ipsum blah blah blah` will translate lorem ipsum through 3 languages then back to English.
  * Possible result: Lorem ipsum is translated to Swedish, then the Swedish translation is translated to Russian, the Russian translation to Esperanto, and the Esperanto translation to English.
  
* **`/magic8ball`**: What will it say?

* **`/clear`**: Send a long blank message to clear the chat.

* **`/boteval <python_code>`**: Runs `eval(<python_code>)` and prints the output.

* **`/ping`**: pong.

### Restricted commands
These can only be run by people who are in the owners array in `bot_info.json`!
 
* **`/botexec [format] <python_code>`**: Runs `exec(<python_code>)` and prints the output. Pretty dangerous. It's almost like SSH, but not quite. Someone used this once to do `sudo apt update` on my PC!
  * `[format]` determines how the output will look. 
    * `-e` will make the output be put in an embedded message.
    * `-n` will make the output not be stylized.
    * Not providing a `[format]` will make the output be monospace.
    
* **`/reload [module]`**: Reload a module/extension/cog. Only useful for developers who want to test changes.
  * `/reload survey`: will cause the survey cog to be reloaded.
  * `/reload`: will reload all cogs.

* **`/pull`**: Runs `git pull`. This is how Adam made his updates to the bot live.
- - - -
## Installation
* Install `discord.py` (tested with v1.3.2).
* Clone this repo and create a file in it called `bot_info.json`.
  * "owners" are people who have access to restricted commands.
  * Here's what it should look like:
```
     {
      "owners":             ["Discord User ID", "Another Discord User ID", ...]
      "login":              "Your Discord app token goes here"
      "yandex-translate":   "Yandex.Translate API key goes here"
     }
```
* Run lounge_bot.py
