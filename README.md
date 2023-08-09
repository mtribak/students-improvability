# Source:
Paulo Cortez, University of Minho, Guimares, Portugal, http://www3.dsi.uminho.pt/pcortez

# Data Set Information:
This data approaches student achievement in secondary education of two Portuguese schools. The data attributes include student grades, demographic, social and school related features, and it was collected by using school reports and questionnaires.

# Run application
## Run on local
```
streamlit run app/daschboard.py
```

## Build a Docker image
```
docker build -t streamlit .
```

## Run on docker container
```
docker run -p 8501:8501 streamlit
```

![Screenshot](ui.png)
