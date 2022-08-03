# Deploy a Python (Django) web app container to Azure App Service

This Python app is a restaurant review application using the [Django](https://www.djangoproject.com/) framework. The app is intended to be used as a container running on  Azure App Service with a connection to a Azure Cosmos DB API for MongoDB. When deployed, Azure managed identity allows the App Service to pull container images from an Azure Container Registry. MongoDB connection info is passed to the code through environment variables. 

This sample app can be run locally and then deployed to Azure, hosted in a fully managed Azure App Service. For more information on how to use this web app, see the  [TBD](TBD).

If you need an Azure account, you can [create on for free](https://azure.microsoft.com/free/).

A Flask sample application with similar functionality is at [TBD](TBD).

## Run and deploy options

Here are some ways you can run the sample web app in this repository.

| Scenario | As-is code        | Container |
| ----------- | ----------- | ----------|
| Local environment | Run repo code in virtual environment with *requirements.txt*. Set environment variables in shell before running. | Build image from repo and run locally in Docker container. Pass environment variables in Docker CLI command or with VS Code task definition <sup>1<sup>. |
| Azure App Service [Web App for Containers](https://azure.microsoft.com/services/app-service/containers/) | Deploy repo code to App service. Set environment variables as App Service configuration settings. | Build image locally or in Azure and push to container registry like Azure Container Registry. Configure App Service to pull from registry. Set environment variables as App Service configuration settings. |
| [Azure Container Apps](https://docs.microsoft.com/azure/container-apps/overview) | *n/a* |  Build image locally or in Azure and push to container registry like Azure Container Registry. Create a Container App with deployment from the registry. Configure environment variables for the container. |

(1) The *.vscode* directory *settings.json* and *tasks.json* are configured either a MongoDB local connection or Azure Cosmos DB connection. The tasks and templates in *.vscode* are only used when using Visual Studio Code locally.

The Web App for Containers scenario is covered in the tutorial [TBD](TBD).

The sample code requires the following environment variables passed in as described in the scenario table above.

```
CONNECTION_STRING=<connection-string>
DB_NAME=restaurants_reviews
COLLECTION_NAME=restaurants_reviews
```

For a local MongoDB instance, the connection string is of the form `mongodb://127.0.0.1:27017`. An Azure Cosmos DB API for MongoDB connections string is of the form `mongodb://<server-name>:<password>@<server-name>.mongo.cosmos.azure.com:10255/?ssl=true&<other-parameters>`.

This app was designed to be containerized and run on App Service. If you want to deploy to App Service without containerizing it first, then be sure to set the *subpath* setting so that App Service finds the *manage.py* in the *azureporject* folder.

## Requirements

The [requirements.txt](./requirements.txt) has the following packages:

| Package | Description |
| ------- | ----------- |
| [Django](https://pypi.org/project/Django/) | Web application framework. |
| [gunicorn](https://pypi.org/project/gunicorn/) | Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX. |
| [pymongo](https://pypi.org/project/pymongo/) | The PyMongo distribution contains tools for interacting with MongoDB database from Python. |
| [requests](https://pypi.org/project/requests/) | An HTTP library |
| [whitenoise](https://pypi.org/project/whitenoise/) | Static file serving for WSGI applications, used in the deployed app. <br><br> This package is used in the [azureproject/settings.py](./azureproject/azureproject/settings.py) file. |

