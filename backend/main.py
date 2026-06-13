from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.analyzer import MalwareAnalyzer
from deobfuscator import PHPDeobfuscator
import uvicorn

# Initialize the FastAPI app
app = FastAPI(
    title="PHPSentinel: Malware Intelligence Platform",
    description="Real-time semantic deobfuscation and malware detection using CodeBERT."
)

# Enable CORS for your React Frontend (standard development port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Analyzer (this loads the CodeBERT model into memory)
analyzer = MalwareAnalyzer()

@app.get("/")
async def root():
    return {"message": "PHPSentinel API is running. Send a POST request to /scan to analyze PHP code."}

@app.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    """
    Endpoint to upload and analyze a PHP file.
    Addresses Research Question 4 regarding the effectiveness of 
    transformer models in real-world server environments.
    """
    # 1. Validate file extension
    if not file.filename.endswith(".php"):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only .php files are accepted for semantic analysis."
        )

    try:
        # 2. Read the file content
        content = await file.read()
        decoded_code = content.decode("utf-8")

        # --- 3. THE NEW DEOBFUSCATION LAYER ---
        cleaner = PHPDeobfuscator()
        cleaned_code = cleaner.clean(decoded_code)

        # 4. Perform the analysis (Transformer Pass + Risk Management) on the CLEANED code
        analysis_results = await analyzer.analyze_code(cleaned_code)

        # 5. Return the structured intelligence
        return {
            "success": True,
            "filename": file.filename,
            "results": analysis_results,
            "deobfuscated_code": cleaned_code  # Added so your React UI can display it!
        }

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Could not decode file. Ensure it is a valid text-based PHP file.")
    except Exception as e:
        # Log error for thesis evaluation purposes
        print(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal analysis engine error.")

if __name__ == "__main__":
    # Start the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)