# TradArch - Document to Markdown Converter

Simple webapp to convert documents to Markdown using markitdown.

## Structure

- `backend/` - Python Flask API
- `frontend/` - React + MUI interface

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Docker Build

```bash
cd backend
docker build -t tradarch-backend .
docker run -p 5000:5000 tradarch-backend
```

## Azure Container Deployment

### Build and push to Azure Container Registry
```bash
az acr login --name <your-acr-name>
docker tag tradarch-backend <your-acr-name>.azurecr.io/tradarch-backend:latest
docker push <your-acr-name>.azurecr.io/tradarch-backend:latest
```

### Deploy to Azure Container Instances
```bash
az container create \
  --resource-group <your-rg> \
  --name tradarch-backend \
  --image <your-acr-name>.azurecr.io/tradarch-backend:latest \
  --dns-name-label tradarch-api \
  --ports 5000
```

### Update frontend API URL
Set `REACT_APP_API_URL` to your Azure container URL before building:
```bash
export REACT_APP_API_URL=http://tradarch-api.<region>.azurecontainer.io:5000
npm run build
```

Deploy the `build/` folder to Azure Static Web Apps or Azure App Service.
