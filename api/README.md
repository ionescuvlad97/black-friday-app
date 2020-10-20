# Documentation for Black Friday Scraper API

The API runs on port 5000 of localhost \
All responses will be in `JSON` fromat

# Start the API service

Open `PowerShell` or `CMD` in the directory where the `docker-compose.yml` is
located, then type: \
`docker-compose exec bf_api python ./bf_api.py`

## Available information

- Companies
- Products Types
- Products
- Products Prices

## Debugging fields

### List all companies

#### Definition

- `GET /debugging/companies`

#### Response

- `200 if ok`
