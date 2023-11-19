<h1 align="center" id="title">Loggleplex</h1>

<p id="description">LogglePlex is a versatile log management platform designed to streamline log ingestion and querying processes. Using a FastAPI server logs are efficiently ingested through a secure POST endpoint and seamlessly uploaded to Elasticsearch for storage. At the heart of LogglePlex is its user-friendly Query UI offering an accessible interface for users to interact with their logs effortlessly. The Query UI features dynamic filters accessible through intuitive buttons allowing users to refine their queries based on specific parameters such as timestamp log level or custom criteria. Its hosted on vercel at</p>
<p>
Project is hosted at vercel to access online
https://loggleplex.vercel.app/</p>
<h2>High Level Architecture</h2>

<img src="https://i.imgur.com/DwaP92Q.png" alt="project-screenshot" width="850" height="400/">

<h3>Log Ingestion</h3>

<p>LogglePlex allows users to upload JSON log files, providing a straightforward method for bringing external log data into the system.
The FastAPI server processes and validates the uploaded log files, ensuring data integrity before ingestion.</p>

<h3>Vercel FastAPI HTTP Server<h3>

<p>The FastAPI server, hosted on Vercel, acts as the backbone for handling HTTP requests and managing log ingestion.
It provides a secure and efficient environment for processing user interactions, such as log file uploads.</p>
<h3>AWS OpenSearch (Elasticsearch)</h3>

<p>Log data, after validation, is ingested into AWS OpenSearch, which functions as the Elasticsearch database.
AWS OpenSearch provides a scalable and reliable solution for storing, indexing, and retrieving log data, ensuring optimal performance.</p>
<h3>Query Builder UI</h3>

<p>LogglePlex features a user-friendly Query Builder UI within the web application.
Users can construct queries using an intuitive blocks interface, selecting dynamic filters to define parameters for log retrieval.</p>
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Log ingestion through http server
*   Robust Query builder
*   Result download

<h2>🛠️ Installation Steps:</h2>

<p>1. Install dependencies</p>

```
pip install requirements.txt
```

<p>2. change the host server and port to 3000</p>

```
http://127.0.0.1:3000
```

<p>3. run the server.py file</p>

```
py run server.py
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   AWS
*   ElasticSearch
*   Vercel
*   Python
*   Fastapi
*   Javascript
*   HTMX