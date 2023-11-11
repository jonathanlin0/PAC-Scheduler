# PAC Scheduler

This code helps you automatically schedule all of your PAC sessions (formally known as Dean's tutoring).

### Setup:
Run `pip3 install -r requirements.txt` in your terminal. This installs all the necessary packages for the python script.

Set up `inputs.txt`. The `inputs.txt` file contains the appointments that you want the script to set up separated by new lines. It should be in the following format:

```
<year>/<month>/<day> <start_hour>:<end_minute> <am/pm> <end_our>:<end_minute> <am/pm> <student being tutored> <description>
```
The <description> part can be anything you want. Typically, the description contains the class that you are tutoring for and the location.
Example `inputs.txt`:
```
2023/01/01 1:00 pm 2:00 pm CS38; location: Lloyd
2023/02/04 2:00 pm 3:00 pm CS38; location: Lloyd
2023/03/05 3:00 pm 4:00 pm CS38; location: Lloyd
```
Note: make sure the month and days are always 2 digits long. For example, January 1st should be `2023/01/01` and not `2023/1/1`. Also, student names should be 2 words.

Set up `names.txt` file. This file contains your name.

Example `names.txt`:
```
John Doe
```

### Run
Open up terminal and navigate to the folder with this repository's contents. Run `python3 main.py` in your terminal. This will open up a browser window and automatically schedule all of your appointments.

### Other Notes:
`past_appts.json` keeps track of all your past appointments. This is useful because the script will not schedule appointments that you have already scheduled. So each time you want to add an appointment, simply add the new appoointments to `input.txt`, and you don't have to worry about deleting past appointments.