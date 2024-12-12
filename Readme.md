# Freedom AI Chatbot (Scott)

## Overview
The Freedom AI Chatbot is a Dockerized application designed to provide AI-powered conversational capabilities. Built using React, Flask, Python, LlamaIndex, and OpenAI, the chatbot can engage users in meaningful conversations and automate responses. The application comprises four main services:

- Admin Interface: A React.js frontend for administrators/ sales executives to chat with users.
- Backend API: A Flask-based backend to handle API requests.
- Database: A MySQL database to store data.
- AI Chatbot Service: A Python service utilizing LlamaIndex and OpenAI for AI functionalities.

## Prerequisites

Before setting up the project, ensure that you have the following installed on your server:

- Operating System: Ubuntu 20.04 LTS or a compatible Linux distribution.
- CPU: Dual-core processor (e.g., 2 vCPUs).
- Memory: 4 GB RAM.
- Storage: 30 GB SSD.

## Firewall Policy
Configure your firewall to allow incoming traffic on the necessary ports:

- Admin Interface: TCP port 80 (HTTP).
- Backend Service: TCP port 5000.
- Chatbot Service: TCP port 5001.
- Database Service: TCP port 3307 (typically not exposed externally for security reasons).

## Steps to Set Up the Project on a New Server

1.  Install Dependencies
    Update package lists and install required packages:
    ``` # Update package lists
    sudo apt-get update

        # Install Nginx
        sudo apt-get install nginx

        # Install Docker
        sudo apt-get install docker.io

        # Install Docker Compose
        sudo apt-get install docker-compose

        # Install Node.js and npm
        sudo apt-get install nodejs npm
        ```

2.  Configure Nginx
    Nginx will serve as a reverse proxy to route incoming requests to the appropriate services.

Navigate to Nginx Configuration Directory
`    cd /etc/nginx/sites-available
   `

Create and Configure admin.conf
`    sudo nano admin.conf
   `

Add the following configuration:

etc/nginx/sites-available/admin.conf

```
    server {
        listen 80;
        server_name YOUR_SERVER_IP_OR_DOMAIN;

        location / {
            proxy_pass http://localhost:3200;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
```

Enable the site by creating a symbolic link:
`    sudo ln -s /etc/nginx/sites-available/admin.conf /etc/nginx/sites-enabled/
   `

Create and Configure backend.conf
`    sudo nano backend.conf
   `

**Add the following configuration:**

```
server {
listen 5000;
server_name YOUR_SERVER_IP_OR_DOMAIN;

    location / {
        proxy_pass http://localhost:6000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:

```
sudo ln -s /etc/nginx/sites-available/backend.conf /etc/nginx/sites-enabled/
```

Create and Configure chatbot.conf

```
sudo nano chatbot.conf
```

**Add the following configuration:**

```
server {
listen 5001;
server_name YOUR_SERVER_IP_OR_DOMAIN;

    location / {
        proxy_pass http://localhost:6001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:
`    sudo ln -s /etc/nginx/sites-available/chatbot.conf /etc/nginx/sites-enabled/
   `

**Test and Reload Nginx Configuration**
- `sudo nginx -t`
- `sudo systemctl reload nginx`

3. Update Twilio Webhook URL
   If you're integrating with Twilio, update the webhook URL to point to your backend service.

Login to Twilio Dashboard.

Navigate to your phone number settings and select `Configure`.

Under "Messaging", update the "Webhook" URL:

`http://YOUR_SERVER_IP_OR_DOMAIN:5000/receive-respond`

4. Clone the Repository

```
git clone git@github.com:Freedom-Property-Investors/ai-sms-portal.git ./freedom-chatbot
```

5. Navigate to the Repository Folder

`cd freedom-chatbot`

6. Configure Environment Variables
   Create a .env file in the chatbot directory to store environment variables.

```
cd chatbot
nano .env
```

Add the following variables:
`    JWT_SECRET_KEY=your_jwt_secret_key
    OPENAI_API_KEY=your_openai_api_key
   `
Note: Replace your_jwt_secret_key and your_openai_api_key with your actual keys.

7. Set frontend url for socket to access
   `cd backend` `sudo nano config.py`

```
FRONTEND_BASE_URL = "current frontend url"
```

8. Create utills.js in admin/src with following content:

   ```
   import axios from "axios";

   const baseURL = "http://ip-address-of-backend:5000/";

   const formatDate = (dateString) => {
   const date = new Date(dateString);
   const day = date.getDate().toString().padStart(2, "0");
   const month = (date.getMonth() + 1).toString().padStart(2, "0");
   const year = date.getFullYear();
   return `${year}-${month}-${day}`;
   };

   function getCookie(name) {
   const cookies = document.cookie.split(";");
   for (let cookie of cookies) {
       const [cookieName, cookieValue] = cookie.split("=");
       if (cookieName.trim() === name) {
       return cookieValue;
       }
   }
   return null;
   }
   function getMonthName(monthNumber) {
   const date = new Date(Date.UTC(2000, monthNumber - 1, 1)); // Subtract 1 because month numbers are zero-based in JavaScript Date objects
   const monthName = date.toLocaleString("default", { month: "long" });
   return monthName;
   }

   const axiosInstance = axios.create({
   baseURL: baseURL,
   });

   export { formatDate, getCookie, getMonthName, axiosInstance, baseURL };
   ```

9. Build Docker Images

`docker-compose build`

10. Start Services

`docker-compose up -d`

## Services

- Admin Interface

  - Description: React.js frontend for administrators.
  - Access URL: http://YOUR_SERVER_IP_OR_DOMAIN
  - Port: 80 (proxied to 3200 internally)

- Backend API

  - Description: Flask backend handling API requests.
  - Access URL: http://YOUR_SERVER_IP_OR_DOMAIN:5000
  - Port: 5000 (proxied to 6000 internally)

- AI Chatbot Service

  - Description: AI service utilizing LlamaIndex and OpenAI.
  - Access URL: http://YOUR_SERVER_IP_OR_DOMAIN:5001
  - Port: 5001 (proxied to 6001 internally)

- Database

  - Description: MySQL database service.
  - Port: 3307 (mapped from container's 3306)

## Accessing the SQL Database

To access the MySQL database inside the Docker container, run:

```
docker exec -it freedom-sms-database mysql -u root -p freedom_db
```

**Note:** You will be prompted to enter the MySQL root password, which is specified in your docker-compose.yml file under MYSQL_ROOT_PASSWORD.

## Technologies Used

- **Frontend:** React.js
- **Backend:** Python Flask
- **Database:** MySQL
- **AI Libraries:** LlamaIndex, OpenAI API
- **Services:** Twilio API (for messaging)
- **Containerization:** Docker, Docker Compose
- **Web Server:** Nginx
- **Environment Management:** Python dotenv

## Environment Variables

- The application relies on several environment variables for configuration. These should be set in a .env file within the chatbot directory.

- JWT_SECRET_KEY: Secret key for JWT authentication.
  OPENAI_API_KEY: API key for accessing OpenAI services.
  Example .env file:

- Ensure all dependencies are correctly specified in requirements.txt.
  Check Docker logs using docker-compose logs for error details.

## Service Not Accessible

Verify that the service is running using docker-compose ps.
Check firewall settings to ensure the required ports are open.
Ensure Nginx is properly proxying requests to the correct ports.
## Database Connection Issues

- Confirm that the database container is running.
- Verify the database credentials in your application configuration.
- Check logs using docker-compose logs mysql.

## Additional Notes

### Security Considerations

Avoid exposing the database port externally unless necessary.
Use strong, unique passwords for database access.
Consider setting up SSL/TLS for secure communication.

### Scaling and Performance
For production environments, consider using a more robust setup with load balancing.
Monitor resource usage and adjust server specifications as needed.

### Logging and Monitoring
Implement logging for all services to monitor activity and troubleshoot issues.
Use tools like ngrep or tcpdump to inspect network traffic if necessary.

### Contact Information
For support or contributions:

- **Author:** aayushi678
- **GitHub:** https://aayushi678@github.com
- **Email:** aayushi@freedompropertyinvestors.com.au

### Acknowledgments
- OpenAI for providing the AI API.
- LlamaIndex for the indexing library.
- Twilio for messaging services.
