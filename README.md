
python -m venv venv 
venv/bin/activate 
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

Then in a second terminal:

cd subvampire-slayer/frontend

python3 -m http.server 3000

## Testing
1. Click "Download Demo Statement" inside the app to get a test CSV
2. Upload it and click "Analyze Now"
3. Or click "Load Demo Instantly" to skip the upload step

repository : https://github.com/bhaktivankhade09-collab/innovexa.git
 Link : https://bhaktivankhade09-collab.github.io/innovexa/
