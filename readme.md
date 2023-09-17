 # GroceryStore

An online grocery store built using Flask and it's extensions for SQLite .

## How to run the application
1. Open the terminal at the root folder

2. Run the `main.py` file using the following command: `python main.py`

## Technologies used
- Python v3.7.3
- HTML5, CSS3, JavaScript
- Bootstrap v5.1.3, v3.4.1

## Folder structure and important files
- `main.py` is the main entry point of the app.
- `README.md` is literally the file you are reading right now.
- `/templates/` contains the HTML templates used for rendering views on the server.
- `/static/` contains the static resources like CSS and JS files necessary for functionality of the app. It also contains some media related to the app.
- `/app/` contains the main components of the application.
- `/app/config/` contains all the configurations / constants required to run the application. Any parameters can be directly changed in one of the files within the folder.
- `/app/controller/` contains the function declarations and all the routes at which the views will be rendered by `flask` and `jinja2`.
- `/app/models/` contains the object models of the various schemas declared in the database.
