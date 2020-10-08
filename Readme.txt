Instructions to run the project
1. extract project file to some location, then extract gameAPI (main project).
2. install all the modules mentioned in requirements.txt
  eg. from command line you can type: "pip install -r requirements.txt"
3. Navigate to gameAPI directory (eg. C:\Users\Kunal\Desktop\gameAPI)
4. run django server using command: "python manage.py runserver"

URL's which are accessible
1. http://127.0.0.1:8000  (to play game)
2. http://127.0.0.1:8000/api  (for api related instructions)
3. http://127.0.0.1:8000/api/player-list/  (to see the list of all players who played)
4. http://127.0.0.1:8000/api/player/<playerId>

All the API responses will be printed to the browser's console.
It is advised to use the latest chrome browser
SQLite3 db is attached as well

if you are not able to get the project running, 
please look at https://connect4dj.herokuapp.com/ 
