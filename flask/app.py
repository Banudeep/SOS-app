from flask import Flask, request, jsonify
from pymongo import MongoClient
import base64
import io
import numpy as np
from PIL import Image
import tensorflow as tf 
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
# from tensorflow.keras.models import load_model
import google.generativeai as genai

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://banudeepreddy:Hello%40890@cluster0.m9gox.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["test"]
collection = db["ambulances"]  

Gemini_API_KEY = "AIzaSyBi0dvebVigXIIpCZoukGCswaD6_xjO-oA"
genai.configure(api_key=Gemini_API_KEY)


# AWS S3 Bucket details
bucket_name = "s32-mlmodel"
object_key = "CNNAccident1.h5"

# Initialize S3 Client
s3 = boto3.client("s3")

# Fetch the model file from S3 into memory
response = s3.get_object(Bucket=bucket_name, Key=object_key)
model_data = response["Body"].read()  # Read file into memory

# Save the model to a temporary file and load it
with tempfile.NamedTemporaryFile(suffix=".h5") as temp_model:
    temp_model.write(model_data)  # Write data to temp file
    temp_model.flush()  # Ensure data is written before reading

    # Load the model from the temporary file
    model = tf.keras.models.load_model(temp_model.name, compile=False)

def generate_first_responder_message(accident_data):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        location = accident_data.get('location', 'Unknown location')
        timestamp = accident_data.get('timestamp', 'Unknown timestamp')
        severity = accident_data.get("PredictedClass", "unprdedicted class")
        injury_part = accident_data.get('body_parts', 'Unspecified injury part')
        text_description = accident_data.get('textDescription', 'No additional description provided')

        prompt = (f"Timestamp: {timestamp}, Severity: {severity}, "
                  f"Location: {location},  Injury: {injury_part}, "
                  f"Description: {text_description}. Provide a concise message for first responders, "
                  "including potential injuries,time of incident, immediate actions, and nearest hospital location.")

        response = model.generate_content(prompt)
        text_response = response.candidates[0].content.parts[0].text

        return jsonify({"message": text_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai_agent', methods=['POST'])
def ai_agent_endpoint():
    accident_data = request.get_json()
    if not accident_data:
        return jsonify({'error': 'No data provided'}), 400

    response = generate_first_responder_message(accident_data)
    return response

def extract_body_parts(text):
    tokens = word_tokenize(text.lower())

    # Reference WordNet synset for body parts
    body_part_synsets = [wordnet.synset("head.n.01"), wordnet.synset("leg.n.01"), 
                         wordnet.synset("arm.n.01"), wordnet.synset("shoulder.n.01"), 
                         wordnet.synset("spine.n.01"), wordnet.synset("chest.n.01"),
                         wordnet.synset("knee.n.01"), wordnet.synset("wrist.n.01")]

    def is_body_part(word):
        word_synsets = wordnet.synsets(word, pos=wordnet.NOUN)  
        for synset in word_synsets:
            for body_part in body_part_synsets:
                if synset.wup_similarity(body_part) and synset.wup_similarity(body_part) > 0.5:
                    return True
        return False


    body_part_keywords = list(set(word for word in tokens if is_body_part(word)))
    return body_part_keywords

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Flask Image API"}), 200

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.json
        if "image" not in data:
            return jsonify({"error": "Image content (Base64) is required"}), 400
        if 'accidentID' not in data:
            return jsonify({"error": "Accident ID is required"}), 400
        
        try:
            image_bytes = base64.b64decode(data["image"].split('base64,')[1])
        except Exception:
            return jsonify({"error": "Invalid Base64 encoding"}), 400
        try:
            image = Image.open(io.BytesIO(image_bytes))
        except Exception:
            return jsonify({"error": "Invalid image data"}), 400
        print("Reached till efore image processing")

        image = image.resize((128, 128))  # Resize if needed
        image_array = np.array(image) / 255.0  # Normalize
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

        # ✅ Predict using the model
        prediction = model.predict(image_array)
        predicted_class = np.argmax(prediction)  # Get class with highest probability


        # ✅ Store in MongoDB
        image_data = {
            "accidentID": data['accidentID'],
            "PredictedClass": int(predicted_class)
        }

        # Search for a document by accidentID
        document = collection.find_one({"accidentID": data['accidentID']})
        new_data = {"PredictedClass": int(predicted_class)}  # Replace with actual image data
        if document:
            # Update the document if it exists
            collection.update_one({"accidentID": data['accidentID']}, {"$set": new_data})
        else:
            collection.insert_one(image_data)
        return jsonify({
            "accidentID": data['accidentID'],
            "PredictedClass": int(predicted_class) # Convert NumPy int to normal int
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/report', methods=['POST'])
def store_report():
    try:
        data = request.json
        if 'accidentID' not in data:
            return jsonify({"error": "Accident ID is required"}), 400
        
        # ✅ Check if `report` field is present
        if "report" not in data:
            return jsonify({"error": "Accident report text is required"}), 400

        accident_report = data["report"]
        extracted_body_parts = extract_body_parts(accident_report)  # Extract body parts

        # ✅ Store in MongoDB
        report_data = {
            "accidentID": data['accidentID'],
            "body_parts": extracted_body_parts
        }

        # Search for a document by accidentID
        document = collection.find_one({"accidentID": data['accidentID']})
        new_data = {"body_parts": extracted_body_parts}  # Replace with actual image data
        if document:
            # Update the document if it exists
            collection.update_one({"accidentID": data['accidentID']}, {"$set": new_data})
            print("Document updated successfully")
        else:
            collection.insert_one(report_data)

        return jsonify({
            "accidentID": data['accidentID'],
            "body_parts": extracted_body_parts
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
