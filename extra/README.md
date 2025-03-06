# Extra (Selenium-chrome-base)
Add friend Run in batch 10 added user for 1 userId
------------------------------------------------
Requirement
- cookies (for adding friend)
- userId (all cookies will be add to userId)

How to use
- add userId to user_id_for_add.txt 
 - if you want like 10 people will add this userId just put userId to 1 lines
- cookies file should add like 1000+ cookies or much as you can
- setting in addFriend.py
 - max_user_ids = line in file user_id_for_add.txt (1 lines = 1)
 - max_cookies = 10 * line in file user_id_for_add.txt

Recieve Friend
------------------------------------------------
Requirement
- cookies (Id that already have user added)

How to use
- put cookies to file then run

Favorite game
------------------------------------------------
Requirement
- cookies

How to use
- put cookies to file then run
- You can change which game you want using id game in variable "game_ids" in file favorite-selenium.py

CODED BY CHATGPT // THIS REPOSITORY PROVIDED FOR EDUCATION ONLY.