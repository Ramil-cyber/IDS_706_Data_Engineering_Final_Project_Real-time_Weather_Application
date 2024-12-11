# Final Project
.
# How to Run the Streamlit Dashboard

## Step 1: Install Required Libraries
To ensure you have all the necessary libraries, run the following commands in your terminal or command prompt:
```bash
pip install streamlit
pip install folium
pip install streamlit-folium
```

## Step 2: Install Required Libraries
1. Open a terminal or command prompt in the directory where your Python file (new_main.py) is saved.
2. Run the following command:
```bash
streamlit run new_main.py
```
## Step 3: View the Dashboard
Open the Local URL (e.g., http://localhost:8501) in your web browser to view the dashboard.


## Load Test and Quantitative Assessment 

![alt text](images/load_test.png)

•	Load_test.py: we created this script to conduct load testing to evaluate our weather application's performance. 
•	We used Locust to perform the load testing, to verify the microservice's performance. The testing result shows that when scaling to 10,000 concurrent users, our microservice demonstrates strong system reliability and stability, with the service maintaining a consistent 0% failure rate throughout the testing duration while handling approximately 1,800-2,000 requests per second (RPS). The reason why the actual RPS is below our 10,000 RPS target is because OpenWeather API sets a free tier limit of 2,000 calls per day, resulting this bottleneck for the performance. However, as evidenced by the steady RPS graph maintaining around 1,800-2,000 requests per second once reaching peak load and a consistent response time pattern, our system exhibits excellent stability. 
