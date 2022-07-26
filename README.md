# Deploy a Python (Django) app to Azure with Managed Identity 

This Python app is a restaurant review application using the [Django](https://www.djangoproject.com/) framework. The app is intended to be used as a container running on  Azure App Service with a connection to a Azure Cosmos DB API for MongoDB. When deployed, Azure managed identity allows the App Service to pull container images from an Azure Container Registry. MongoDB connection info is passed to the code through environment variables. 

This sample app can be run locally and then deployed to Azure, hosted in a fully managed Azure App Service. For more information on how to use this web app, see the  [TBD](TBD).

If you need an Azure account, you can [create on for free](https://azure.microsoft.com/free/).

A Flask sample application with similar functionality is at [TBD](TBD).

## Requirements

The [requirements.txt](./requirements.txt) has the following packages:

| Package | Description |
| ------- | ----------- |
| [Django](https://pypi.org/project/Django/) | Web application framework. |
| [gunicorn](https://pypi.org/project/gunicorn/) | Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX. |
| [pymongo](https://pypi.org/project/pymongo/) | The PyMongo distribution contains tools for interacting with MongoDB database from Python. |
| [requests](https://pypi.org/project/requests/) | An HTTP library |
| [whitenoise](https://pypi.org/project/whitenoise/) | Static file serving for WSGI applications, used in the deployed app. <br><br> This package is used in the [azureproject/settings.py](./azureproject/azureproject/settings.py) file. |
