#Web App
This is a functional web applicaiton that have several features:
1. Submit a reading.
2. Display the factorials of all readings ordered by timestamp.
3. Automatically generate ID to readings. 
4. Search all submissions by the reading.

The backend is built with FastAPI and the frontend is built with React, partly follwing the tutorial by Eric Roby (https://www.youtube.com/watch?v=0zb2kohYZIM).

#How to run the app

1. clone the repository
git clone https://github.com/xuliu15/webapp.git

2. Set up virtual environment
python3 -m venv myenv

source myenv/bin/activate

3. Install packages
pip install -r requirements.txt

4. Activate backend
cd FastAPI
uvicorn main:app --reload

5. Activate frontend
cd React/webapp
npm start   

#How to run unit test
cd FastAPI
python3 -m unittest





