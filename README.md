# CS50x_finalProject
### Checkpoint
#### Video Demo: <https://youtu.be/ftSOzgp6T1k>
#### Description:
Checkpoint is a web-app inspired by the the 2024 CS50-X Finance PS.
The purpose of this app is to keep track in a very simple & user-friendly way of two separate things: user's <b>to-do</b> lists and <b>expenses.</b>
Based on a SQL cloudserver, and with a mobile adaptive HTML code, the user can login into this app from multiples devices, inserting an expense while wating for the grocery checkout or comfortable looking at monthly expense analysis . 

#### Folder/File: 
- _app.py_: this is the main py file that structures the file. Webpages are here rendered through Flask, while all the database side is managed through sqlite3.
- _helpers.py_: imported to get some functions like login required and other functions involved in string comparison and SQL operations
- _requirements.txt_: list of all package involved in the project
- _fp.db_ : SQL DB with 3 linked tables: USERS, with id, username, and hash(psw); EXPENSES, with id,username, category, description, amount, and timedate; TODOS, with id, username, category, item, status, and timedate.
- static/_styles.css_: CSS contribution to the web-pages
- static/_logic.js_: JavaScript contribution to the HTML
- templates/_layout.html_: general layout of the webapp. all other html pages are blockmain within this masterpage.
- templates/_register.html_: registration interface. take a (unique) username, and a password. Registration authomatically accepted if no errors. 
- templates/_login.html_: login interface, standard username and password. Login if no errors.
- templates/_apology.html_: customizable error message.
- templates/_index.html_: homepage, greet the user and introduce (with hyperlink) the 4 section of this webapp (below)
- templates/_todo.html_: Section 1: allows user to insert a to-do item, choosing between 'urgent' and 'backlog' cluster. At the bottom of the display, there's a short list that recap last 5 to-do inserted.
- templates/_wordz.html_: Section 2: recap of current active to-do items, split in two tables (urgent and backlog) with the indication of "due days" and a button to remove the item,
- templates/_expense.html_: Section 3: allows the user to insert an expense item, choosing also a spending category (from a predetermined subset). At the bottom of the display, there's a short list that recap last 5 expenses inserted. 
- templates/_numberz.html_: Section 4: after selecting a month, the user can visualize spending detail in a plan table and in month/category chart.


#### General philosopy and future updates:
Checkpoint's DNA means to be something quick and comfy that can be used to keep track of two things that often got messed up in the plannig: an always changing to-do list and expenses made (long tail included!).
Even tho the lightness of Checkpoint is intended, i recognize that few steps can be achieved to make it more useful and more solid.  
Beyond CS50 final project purpose, i will keep updating Checkpoints in my spare times. 

Future updates on which i'm working on:
- add feature to move to-do items between clusters;
- add feature to choose custom category lists;
- add insight generation as 3rd pillar on Numberz, besides table and chart;
- add 5th Section: "Magic Pocket", a cloud space in which store small things: a 1min audio, couple of weblink, a file i need to pass across multiple devices.