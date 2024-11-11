# CS50x_finalProject
### Checkpoint
#### Video Demo:  <URL HERE>
#### Description:

####Languages:
Python, HTML, CSS, JavaScript

####Summary:
Checkpoint is a web-app inspired by the the 2024 CS50-X Finance PS.
The purpose of this app is to keep track in a very simple & user-friendly way of two separate things: user's <b>to-do</b> lists and <b>expenses.</b>
Based on a SQL cloudserver, and with a mobile adaptive HTML code, the user can login into this app from multiples devices, inserting an expense while wating for the grocery checkout or comfortable looking at monthly expense analysis . 

####Folder/File: 
- <u>app.py</u>: this is the main py file that structures the file. Webpages are here rendered thought Flask, while all the database side is managed thought sqlite3.
- <u>helpers.py</u>: imported to get some functions like login required and other functions involved in string comparison and SQL operations
- <u>requirements.txt</u>: list of all package involved in the project
- <u>fp.db</u>: SQL DB with 3 linked tables: USERS, with id, username, and hash(psw); EXPENSES, with id,username, category, description, amount, and timedate; TODOS, with id, username, category, item, status, and timedate.
- static/<u>styles.css</u>: CSS contribution to the web-pages
- static/<u>logic.js</u>: JavaScript contribution to the HTML
- templates/<u>layout.html</u>: general layout of the webapp. all other html pages are blockmain within this masterpage.
- templates/<u>register.html</u>: registration interface. take a (unique) username, and a password. Registration authomatically accepted if no errors. 
- templates/<u>login.html</u>: login interface, standard username and password. Login if no errors.
- templates/<u>apology.html</u>: customizable error message.
- templates/<u>index.html</u>: homepage, greet the user and introduce (with hyperlink) the 4 section of this webapp (below)
- templates/<u>todo.html</u>: Section 1: allows user to insert a to-do item, choosing between 'urgent' and 'backlog' cluster. At the bottom of the display, there's a short list that recap last 5 to-do inserted.
- templates/<u>wordz.html</u>: Section 2: recap of current active to-do items, split in two tables (urgent and backlog) with the indication of "due days" and a button to remove the item,
- templates/<u>expense.html</u>: Section 3: allows the user to insert an expense item, choosing also a spending category (from a predetermined subset). At the bottom of the display, there's a short list that recap last 5 expenses inserted. 
- templates/<u>numberz.html</u>: Section 4: after selecting a month, the user can visualize spending detail in a plan table and in month/category chart.


####General philosopy and future updates:
Checkpoint's DNA means to be something quick and comfy that can be used to keep track of two things that often got messed up in the plannig: an always changing to-do lists and expenses made (long tail included!).
Even tho the lightness of Checkpoint is intended, i recognize that few steps can be achieved to make it more useful and more solid.  
Beyond CS50 final project purpose, i will keep updating Checkpoints at low efforts. 
Even Future updates on which i'm working on:
- add feature to move to-do items between clusters;
- add feature to choose custom category lists;
- add insight generation as 3rd pillar on Numberz, besides table and chart;
- add 5th Section: "Magic Pocket", a cloud space in which store small things: a 1min audio, couple of weblink, a file i need to pass across multiple devices.