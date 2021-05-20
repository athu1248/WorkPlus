# WorkPlus - Our Hackathon Project

## Fun Group name:

Team Bro Code

## Group members:

[Atharva Kulkarni](https://www.linkedin.com/in/atharva-kulkarni-0b292320a?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BMUievu70QISmeuJcTVXlDQ%3D%3D)  
Darshan Shivakumar  
Aditya Sundar  
Debashish Sahoo 

## Video Demonstration
[Video (YouTube)](https://youtu.be/RHhPdILZCoQ)

## Fill in the gaps:


Due to Covid-19, remote working has skyrocketed, especially in the IT industry, leading to an increase in work hours. As a result, fitness, mental health and productivity have taken a massive toll, so our project will aim to solve these underlying issues by building an application that promotes a healthy mode of living in the current working environment.

## Simple description of what your project is and what it does:

WorkPlus is a collaborative platform designed for workplace communication that simultaneously promotes a healthy and fruitful lifestyle for all the employees. Not only does it allow you to share tasks and files with your teammates and communicate with them through an interactive chat window, WorkPlus also enables you to track your personal and team fitness levels and engage in fun, rewarding fitness and trivia challenges, making “work from home” a more enjoyable & productive experience!


### Fitness & Team Bonding features:-

**Connect your Fitbit Account**: WorkPlus allows you to authorize your Fitbit account with your profile, and displays relevant health and fitness data to you and your teammates! 

**Upload your daily Nike Run**: WorkPlus offers a daily 2km running challenge where you can upload a screenshot of your run today using the Nike Run Club App, and our program rewards you with points after proofreading the upload using Python's AI and Image Recognition!

**Trivia of the Day**: WorkPlus assigns you a daily trivia question that rewards you with points when answered correctly!

**Incentive Point System**: WorkPlus has an in-built point system that is used as an incentive to keep workers healthy. Completing tasks like the Nike Run Club daily 2km challenge & the Trivia of the Day reward you with points that get added up to your tally for the month. The point system restarts each month. WorkPlus displays you your current point tally and also the team's cumulative tally. Users do not get to view their peers' points in order to avoid unhealthy competition. The team leader, however, can see everybody's points. At the end of every month, the person with the most points can be rewarded for his efforts, and the company/team has the full freedom to come up with a prize. For instance, one of the best suggestions on behalf of WorkPlus is for the team to donate $1 or ¥100 per point achieved by the team as a whole to a charity in need.

**Check On Your Peers!**: WorkPlus allows you to view your team members' daily steps and sleep hours from their Fitbit accounts.

**Wellness Reminders**: WorkPlus displays you a carousel of facts, suggestions and reminders to keep you fit physically and mentally.


### Workplace features:-

**Chat Feature**: WorkPlus allows you to communicate with your colleagues in a real-time interactive chat window with the help of Django Channels & Sockets!

**Add Project & Tasks**: WorkPlus allows you to add current and upcoming projects along with daily and unfinished tasks for everyone to see.

**Upload Files**: WorkPlus allows you add files to the dashboard for everyone to see.


## Technologies/Software/Programming Languages used:

- Django  
- Python   	   
- HTML    
- CSS     
- JavaScript  

## Detailed instructions for how to open or run your project:

1. Download all the files from the Dropbox.

2. [Register a fitbit app](https://dev.fitbit.com/apps/new) with the following details:
		
		OAuth 2.0 Application Type: Server
		Redirect URL: http://localhost:8000/fitbit
		Default Access Type: Read-Only
		
		Rest of the details required may be added by your own preference
		
	
	_Add your newly created fitbit app's [CLIENT ID](./fitbit/fitbitvars.py#L8) and [CLIENT SECRET](./fitbit/fitbitvars.py#L9) in fitbit/fitbitvars.py and templates/base1.html where specified._
	
3. Open the Terminal on your Mac (Command Prompt on Windows) and run the following lines of code:-


	Use appropriate command to navigate into the project directory: 
 
		cd WorkPlus		#make sure you are in the right folder to begin with


	Activate a virtual environment (Optional): 

		virtualenv env  
                     
		source env/bin/activate		#look for the path to your directory 

	
	Install all the required libraries and packages:
		
		pip install -r requirements.txt
			

	Run the server:

		python3 manage.py runserver   

## License & Code Re-Use
The code for this project is released under the [GPL-3.0 License](./LICENSE). We ask that you please include a link back to this GitHub repository.

## Project official sources

- Fitbit API : https://dev.fitbit.com/build/reference/web-api/
- Bootstrap : https://getbootstrap.com/
- Trivia questions : https://pastebin.com/QRGzxxEy

## Why you may not be able to run our project!
As stated in our sources above, our project uses Fitbit API to retrieve the user's daily activity. Doing so prompts us to apply our client_ID and client secret which is unique for every fitbit app. This is used to obtain the access token to activate the API. But since we are not dishing out any money to host the website on a paid server, the project will not work for anyone unless they have their own client_ID and client secret. We are looking forward to publishing our website online in the near future and hopefully store all our files on a designated hosting service.
	 
