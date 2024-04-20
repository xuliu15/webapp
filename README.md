# Web App

This is a functional web applicaiton that have several features:
1. Submit a reading.
2. Display the factorials of all readings ordered by timestamp.
3. Automatically generate ID to readings. 
4. Search all submissions by the reading.

The backend is built with **FastAPI** and the frontend is built with **React**, partly following the tutorial by Eric Roby (https://www.youtube.com/watch?v=0zb2kohYZIM).

# How to run the app
**Note**: Following steps are only tested on Mac and VS Code.

#### 1. clone the repository
   
`git clone https://github.com/xuliu15/webapp.git`

#### 2. Set up virtual environment

`python3 -m venv myenv`

#### 3. Activate virtual environment

`source myenv/bin/activate`

#### 4. Install packages
   
`pip install -r requirements.txt`

#### 5. Activate backend
   
Go to `cd webapp/FastAPI`

Then `uvicorn main:app --reload`

#### 6. Activate frontend
   
Go to `cd React/webapp`

Then `npm start` 

# How to run unit test

Go to `cd FastAPI`

Then `python3 -m unittest`





