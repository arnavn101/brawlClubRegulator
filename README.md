# BrawlClubRegulator - v2.0

********
***Overview***
********

This repository provides a way to regulate discord servers affiliated to a brawl stars club. In simple terms, it ensures
that all members of the discord server with the "member" role are players with the brawl stars club.

- ``brawlClubAutomator``: a brawl stars discord server regulator
 

Functionality
=====

Fundamentally, ``brawlClubAutomator`` is capable of 
    
    1) Altering Roles & Nicknames of Members based on their BrawlStars profile 
  
    2) Storing DB with player profile linked to discord id
    
    3) Host Tournament and Team enlisting
    
    4) Using BrawlStats and StarList API to get info on the game
    
    5) Other Misc commands (display user avatar, admin tools...)


************
Installation/Configuration
************

Linux Environments
==========================

On any Linux OS, clone this repository and change arguments of config.cfg & 
BrawlStars club information. Also, add Discord Bot Secret and other bot-related info 
in settings.py

      vim config_files/config.cfg # API Keys, Timing Config
      vim config_files/settings.py # Bot Info, prefixes, Secrets
      vim config_files/tags.txt # Add BrawlStars Club Tags
      

Install requirements of Python
    
     python3 -m venv brawlClubEnv
     source brawlClubEnv/bin/activate
     pip install -r requirements.txt
     
Now, there are two choices: 

(1) Directly run the bot in the background:
     
     python3 brawlClubRegulator.py& # Run in background
     
(2) Run the bot as a linux service:

     vim discordbot.service # Specify Directory of the python file 
     sudo mv discordbot.service /etc/systemd/system/ 
     sudo service discordbot start


APIs and Resources Used
===============
      discord.py
      BrawlStats
      dataset
      APScheduler
      # For more, refer to the requirements.txt file

