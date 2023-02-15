apt-get update -y
apt-get install uvicorn -y
apt-get install pip -y
git clone 
cd fastapi_fftt
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 80