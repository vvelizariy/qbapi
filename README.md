# Quick Books API client

## Configuration
To run application, update `.env` file with proper values

```
to get access and refresh tokens you should check, in QuickBooksAPIClient 
self.auth_client.get_bearer_token("code_from_url", settings.REALM_ID)
```

```
QB_CLIENT_ID=QB_CLIENT_ID
QB_CLIENT_SECRET=QB_CLIENT_SECRET
QB_ACCESS_TOKEN=QB_ACCESS_TOKEN
QB_REFRESH_TOKEN=QB_REFRESH_TOKEN
QB_REDIRECT_URI=https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl
QB_REALM_ID=QB_REALM_ID

DB_NAME=qbapi
DB_USER=qbapi
DB_PASSWORD=my_password
DB_ROOT_PASSWORD=my_root_password
```
## Usage
To run application, execute
```
sudo docker compose up --build 
```


Application works in following way:
- if there are no records in DB it fetches all transaction starting from constant defined as DEFAULT_START_DATE
- if there are records, it fetches records with date newer than latest in db
- when user specifies from_date and/or to_date e.g:
```
http://localhost:8000/transactions?from_date=2024-01-03&to_date=2024-03-03
```
it returns csv file with transactions with specified time range,
if range is not specified, returns all transactions

### ToDo

1. Improve errors handling
2. Add logging details
3. Check on prod data if daily transactions fit limit of 400Lakh 
