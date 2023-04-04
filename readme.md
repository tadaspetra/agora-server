# Agora Server for Cloud Recording and Real Time Transcription

## Getting Started

```
pip install flask
```

## Create a `.env` file with the following values
```
CUSTOMER_KEY = "<--Agora Customer Key-->"
CUSTOMER_SECRET = "<--Agora Customer Key-->"

TEMP_TOKEN = "<--Agora Temporary Token-->"
APP_ID = "<--Agora App ID-->"

AWS_SECRET_KEY = "<--AWS Secret Key-->"
AWS_ACCESS_KEY = "<--AWS Access Key-->"
AWS_BUCKET_NAME = "<--AWS Bucket Name-->"
```

## Starting Server

```
python -m flask run 
```

## Interfaces

### Start Cloud Recording
#### Endpoint
```
/start-recording/<--Channel Name-->
```
#### Successful Response
```
{sid: <--SID Value-->, resource_id: <--Resource ID Value-->}
```

### Stop Cloud Recording
#### Endpoint
```
/stop-recording/<--Channel Name-->/<--SID-->/<--Resource ID-->
```
#### Successful Response
```
{}
```

### Start Real Time Transcription
#### Endpoint
```
/start-transcribing/<--Channel Name-->
```
#### Successful Response
```
{taskId: <--Task ID Value-->, builderToken: <--Builder Token Value-->}
```

### Stop Real Time Transcription#### Endpoint
```
/start-transcribing/<--Channel Name-->/<--Task ID-->/<--Builder Token-->
```
#### Successful Response
```
{}
```