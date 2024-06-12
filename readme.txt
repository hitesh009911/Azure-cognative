# Image Analysis Flask Application

This repository contains a Flask web application that integrates with Azure Cognitive Services and Azure Storage to perform image analysis, including object detection, face detection, and tag generation.

## Features

- Upload images to Azure Blob Storage.
- Analyze images for objects, tags, and faces using Azure Cognitive Services.
- Display analysis results with links to Google search for tags.

## Prerequisites

- Python 3.7+
- Azure Subscription
- Azure Cognitive Services (Computer Vision and Face API)
- Azure Storage Account
- Azure Cosmos DB

## Setup

### Clone the Repository

```bash
git clone https://github.com/yourusername/image-analysis-flask-app.git
cd image-analysis-flask-app

Install Dependencies
Create a virtual environment and install the required libraries:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

Configure Azure Services
Azure Cognitive Services
Create a Cognitive Services resource.
Note down the endpoint and key.
Azure Blob Storage
Create a Storage Account in Azure.
Create a container in the storage account.
Note down the storage account name, container name, and account key.
Azure Cosmos DB
Create a Cosmos DB resource.
Create a database and a container.
Note down the endpoint, key, database name, and container name.

Configuration
Rename the config.py.example to config.py and replace the placeholders with your actual Azure credentials:

# Azure Storage configuration
storage_account_name = 'YOUR_STORAGE_ACCOUNT_NAME'
storage_account_key = 'YOUR_STORAGE_ACCOUNT_KEY'
container_name = 'YOUR_CONTAINER_NAME'

# Azure Cognitive Services configuration
cog_services_key = 'YOUR_COG_SERVICES_KEY'
cog_services_endpoint = 'YOUR_COG_SERVICES_ENDPOINT'

# Azure Cosmos DB configuration
cosmosdb_endpoint = 'YOUR_COSMOS_DB_ENDPOINT'
cosmosdb_key = 'YOUR_COSMOS_DB_KEY'
cosmosdb_database_name = 'YOUR_DATABASE_NAME'
cosmosdb_container_name = 'YOUR_CONTAINER_NAME'

Running the Application
Start the Flask application:

set FLASK_APP=app.py
set FLASK_ENV=development
flask run

Deploying to Azure Web App
Create an Azure Web App.
Deploy the application code to the Azure Web App.
Usage
Navigate to http://127.0.0.1:5000 in your web browser.
Upload an image for analysis.
View the analysis results, including detected objects, tags, and faces.
Click on a tag to search for more information on Google.
License
This project is licensed under the MIT License.


### Files to Include in the Repository

- `app.py`: The main Flask application file.
- `config.py.example`: A template configuration file with placeholders.
- `requirements.txt`: A file listing all the dependencies.
- `templates/`: A directory containing HTML templates (`list.html`, `analysis_results.html`, etc.).
- `static/css/`: A directory for CSS files (`style2.css`).
- `README.md`: The generated README file.

### Example `requirements.txt`


This README provides clear instructions on setting up the project, configuring Azure services, and running the application both locally and on Azure Web App. It also includes sample code and templates to ensure everything works seamlessly.
