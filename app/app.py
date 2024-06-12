from flask import Flask, render_template, jsonify, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.core.exceptions import ResourceExistsError
import uuid  # Import the uuid module to generate unique identifiers
import time
import threading
import logging

app = Flask(__name__)

# Azure Blob Storage configuration
storage_account_name = "vini1"
storage_account_key = "EmHFiicyGw1J6F1zar/GCmHHX/2mIABfthMsbC6PxVGGyXM2RmBahl8EwUfL9qPKncku/QSDc37x+ASt/FvieA=="
container_name = "images"

# Azure Cosmos DB configuration
cosmosdb_endpoint = "https://vini.documents.azure.com:443/"
cosmosdb_key = "2qnj1CvfQF7Zi69d85x6PaYoJpZWQI9DOs2K1kNPxc0QF2Pk7umgHRJX0U3D5ZnGb3WzdK1Mnz2BACDbBaDQ2Q=="
cosmosdb_database_name = "image"
cosmosdb_container_name = "cont1"

# Azure Cognitive Services configuration
cog_endpoint = "https://vinicon.cognitiveservices.azure.com/"
cog_key = "8a6343bfbd334aa8b183ae8e3b924354"

face_key = '8fe6cd0d048346f88d8f261b8859e74a'
face_endpoint = 'https://python-face.cognitiveservices.azure.com/'

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(
    f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};")

# Initialize Cosmos DB Client
cosmos_client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)
database = cosmos_client.get_database_client(cosmosdb_database_name)
container = database.get_container_client(cosmosdb_container_name)

# Initialize Computer Vision Client
computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

# Function to simulate delay and then redirect to index
def delayed_redirect():
    time.sleep(2)
    with app.test_request_context():
        return redirect(url_for('index'))

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/loading')
def loading():
    # Start the delay in a separate thread to avoid blocking
    threading.Thread(target=delayed_redirect).start()
    return render_template('loading.html')

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/list')
def new_page():
    blob_list = []  # Initialize an empty list to store blob names
    try:
        time.sleep(2)
        # Get the list of blobs from the Azure Blob Storage container
        blob_list = [blob.name for blob in blob_service_client.get_container_client(container_name).list_blobs()]
    except Exception as e:
        # Handle exceptions if any
        return f"Error: {str(e)}", 500
    return render_template('list.html', blob_list=blob_list)


@app.route('/analyze_blob/<blob_name>')
def analyze_blob(blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    image_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    analysis_results = computervision_client.analyze_image(image_url, visual_features=[VisualFeatureTypes.tags])
    tags = [tag.name for tag in analysis_results.tags]
    return render_template('analysis_results.html', image_url=image_url, tags=tags)

@app.route('/delete_image/<blob_name>', methods=['POST'])
def delete_image(blob_name):
    try:
        # Delete the image blob from Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
        return jsonify({"message": "Image deleted successfully"})
    except Exception as e:
        # Handle any errors that may occur during deletion
        return jsonify({"error": str(e)}), 500



@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        selected_blob = request.form.get('selected_blob')
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=selected_blob)
        image_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{selected_blob}"
        analysis_results = computervision_client.analyze_image(image_url, visual_features=['tags'])
        tags = [tag.name for tag in analysis_results.tags]
        return render_template('analysis_results.html', image_url=image_url, tags=tags)

    blob_list = [blob.name for blob in blob_service_client.get_container_client(container_name).list_blobs()]
    return render_template('list.html', blob_list=blob_list)

@app.route('/upload', methods=['POST'])
def upload():
    # Process uploaded image
    image_file = request.files['image']
    metadata = {'id': str(uuid.uuid4()), 'image_name': image_file.filename}  # Include 'id' property
    try:
        # Upload image to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=image_file.filename)
        if blob_client.exists():
            # If the blob already exists, generate a unique name
            blob_name = generate_unique_blob_name(image_file.filename)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(image_file)

        # Analyze image with Azure Cognitive Services
        image_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_client.blob_name}"
        analysis_results = computervision_client.analyze_image(image_url, visual_features=[VisualFeatureTypes.tags])

        # Extract tags from analysis results
        tags = [tag.name for tag in analysis_results.tags]

        # Store metadata and analysis results in Azure Cosmos DB
        metadata['analysis_results'] = tags
        container.create_item(body=metadata)

        return redirect(url_for('index'))
    except ResourceExistsError:
        # Handle the situation when the blob already exists
        # You can choose to generate a unique name or display an error message
        return "Error: The specified blob already exists.", 409
    except Exception as e:
        # Handle other exceptions
        return f"Error: {str(e)}", 500

def generate_unique_blob_name(filename):
    timestamp = str(int(time.time()))
    return f"{filename}_{timestamp}"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)