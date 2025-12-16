# deposit\_subscription\_prediction\_api

Deposit Subscription Prediction Api (FastAPI)



Pull: docker pull swaraj66/deposit\_subscription\_prediction\_api



Run: docker run -p 8000:8000 swaraj66/deposit\_subscription\_prediction\_api



Access API Documentation: http://localhost:8000/docs



API Endpoint: POST /predict



Example of Request Body (JSON): { "age": 29, "job": "admin", "marital": "single", "education": "tertiary", "default": "no", "balance": 3450, "housing": "yes", "loan": "no", "contact": "cellular", "day\_of\_week": 2, "month": "may", "duration": 210, "campaign": 3, "pdays": 44, "previous": 0, "poutcome": "nonexistent" }



Example Response: { "predicted\_category": 1, "predicted\_probability": 0.39347 }



here: 1->yes 0->no

