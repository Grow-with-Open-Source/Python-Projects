from textblob import TextBlob

def get_correction(text):
    if not text.strip():
        return None, False
    
    blob = TextBlob(text)
    corrected = str(blob.correct())
    
    # Check if the original matches the corrected version
    is_correct = text.lower().strip() == corrected.lower().strip()
    return corrected, is_correct