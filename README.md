# Shorty
This is a CherryPy REST API for URL shortening. For testing convenience the API set to run on localhost:8080, the default CherryPy settings. A Dockerfile is also included if you would like to launch it in a ubuntu container.

* **URL**

  /localhost:8080/api/vi

* **Method:**

  POST - generates shortened url
  GET - returns list of keys/urls stored

*  **URL Params**
  
  None

* **Data Params**

  JSON with the “url” key to define the URL to shortened
  POST - {“url": "http://mylongurl.com"}

* **Success Response:**

  JSON returns with shortened key and url

  Code: 200
  
  POST Content: {“key": "MjIxNTc2ODc0OA==", "shortened_url": "http://localhost:8080/MjIxNTc2ODc0OA=="}
  GET Content: {"MjIxNTc2ODc0OA==", "http://localhost:8080/MjIxNTc2ODc0OA=="}

* **Error Response:**
  
  Code: 404, NOT FOUND

* **Sample Call:**

  curl -X POST -v http://localhost:8080/api/v1 -H "content-type:application/json" -d '{"url": "http://mylongurl.com"}'
  curl -X GET -v http://localhost:8080/api/v1

* **URL**

  /localhost:8080/api/vi/\<url_key\>

* **Method:**

  GET - return the URL for the key
  DELETE - delete the stored url for the key

*  **URL Params**
  
  url_key : shortened url key passed back from POST request

* **Data Params**

  None

* **Success Response:**

  Code: 200
  
  GET Content: {"url": "http://mylongurl.com"}

* **Error Response:**
  
  Code: 404, NOT FOUND

* **Sample Call:**

  curl -X GET http://localhost:8080/api/v1/MjIxNTc2ODc0OA==
  curl -X DELETE http://localhost:8080/api/v1/MjIxNTc2ODc0OA==

* **URL**

  /localhost:8080/\<url_key\>
  
  This does the actual redirect

  Also shortened_url returned in the post response - "http://localhost:8080/MjIxNTc2ODc0OA=="

* **Method:**

  GET

*  **URL Params**
  
  url_key : shortened url key passed back from POST REST API request

* **Data Params**

  None

* **Success Response:**

  Code: 200

* **Error Response:**
  
  Code: 404, NOT FOUND

* **Sample Call:**

  curl -X GET http://localhost:8080/MjIxNTc2ODc0OA==
  
  This resource can be found at <a href='http://google.com'>http://google.com</a>.

  You can also put localhost:8080/MjIxNTc2ODc0OA== in a web browser and have the redirected page come up.

**Docker Configuration**
----

*  **Image Creation from Dockerfile**

  docker build -t restapp/shorty .

  Execute the following command from the same directory as the Dockerfile to create image called restapp/shorty

*  **Run the docker image**

  docker run -d -p 32768:8080 restapp/shorty

  This command starts the container and maps port 32769 on host to port 8080 in the container.

*  **Execute REST API on container**

  My local test scenario was to deploy docker on my mac. In this case, after the container was running, I needed to find the IP address of the container in order send the commands via curl. The docker-machine ls command returns the IP address.

  docker-machine ls
  
  default     *         virtualbox    Running     tcp://192.168.99.100:2376               v1.12.2   

*  **Example REST API's**

  curl -X POST http://192.168.99.100:32768/api/v1 -H "content-type:application/json" -d '{"url": "http://mylongurl.com”}’
  Returns: {"key": "MzEwMDg2Njk0MA==", "shortened_url": "http://shorty.com/MzEwMDg2Njk0MA=="}

  curl -X GET http://192.168.99.100:32768/api/v1/MzEwMDg2Njk0MA==
  Returns: {“url": "http://mylongurl.com"} 

  
