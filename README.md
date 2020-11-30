# mathgo-backend
This is used as the backend for the Math Go project (https://github.com/youncher/mathgo)

## Running the project locally
1. Clone this repository and cd into the project
2. Create python virtual environment: `python3 -m venv venv`
3. Activate the Python virtual environment: `source env/bin/activate`
4. Install requirements: `pip install  -r requirements.txt`
5. Run the application: `python main.py`

## Deploying to Google App Engine
1. Inside main.py, replace `"Enter_Google_Signin_webClientId"` with your Web Client Id.
2. `gcloud app deploy`

## API URL
* Local: http://localhost:8080
* Hosted on Google App Engine: https://mathgo-46d6d.wl.r.appspot.com

## Endpoints
* GET - https://mathgo-46d6d.wl.r.appspot.com
  * Description: Returns a simple string greeting
* POST - https://mathgo-46d6d.wl.r.appspot.com/user/validation
  * Description: Checks if given gid (Google user unique id) is an existing Math Go user.
  * Example request body (JSON):
      <pre><code>
        {
          "gid": "testGoogleUserID_1"
        }
      </code></pre>
  * Example response (JSON):
    <pre><code>
      {
        "avatar": 1, 
        "existingUser": true
      }
      </code></pre>
## Resources
* https://cloud.google.com/appengine/docs/standard/python3/quickstart
