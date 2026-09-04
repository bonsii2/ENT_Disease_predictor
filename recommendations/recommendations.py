"""
Medical Recommendations Knowledge Base.

This module provides general, educational information based on AI predictions.
CRITICAL SAFETY NOTICE:
- All recommendations are strictly for educational and decision-support purposes.
- Never prescribe medication or dosages.
- Never claim the AI result is a definitive medical diagnosis.
"""

RECOMMENDATIONS = {
    # Ear Model Recommendations
    "Acute Otitis Media": {
        "title": "Possible Acute Otitis Media Detected",
        "message": "The AI model predicts patterns consistent with possible acute otitis media (middle ear infection).",
        "advice": "Because ear infections require clinical evaluation, consult a qualified healthcare professional, particularly if there is significant pain, fever, fluid discharge, or worsening symptoms."
    },
    "Cerumen Impaction": {
        "title": "Possible Cerumen Impaction Detected",
        "message": "The model predicts possible earwax buildup (cerumen impaction).",
        "advice": "Avoid inserting objects like cotton swabs into the ear canal. Consider evaluation by a healthcare professional if you experience hearing loss, discomfort, fullness, dizziness, or persistent symptoms."
    },
    "Chronic Otitis Media": {
        "title": "Possible Chronic Otitis Media Detected",
        "message": "The model predicts features suggestive of chronic otitis media.",
        "advice": "Professional medical evaluation by an ENT specialist is recommended because persistent middle-ear issues may require comprehensive otoscopic examination and treatment."
    },
    "Myringosclerosis": {
        "title": "Possible Myringosclerosis Detected",
        "message": "The AI model predicts signs consistent with myringosclerosis (calcification of the eardrum).",
        "advice": "A healthcare professional should evaluate the ear structure to determine whether further investigation or hearing assessment is needed."
    },

    # Nose Model Recommendations
    "Allergic Rhinitis": {
        "title": "Possible Allergic Rhinitis Signs Detected",
        "message": "The AI model identifies visual features common in allergic nasal inflammation.",
        "advice": "Consider discussing nasal congestion, sneezing, or itchy eyes with a primary care doctor or allergist for proper evaluation and personalized advice."
    },
    "Nasal Polyps": {
        "title": "Possible Nasal Polyps Detected",
        "message": "The AI model predicts visual signs associated with nasal mucosal swelling or polyps.",
        "advice": "Consult an Ear, Nose, and Throat (ENT) specialist for clinical examination if you experience persistent nasal obstruction, loss of smell, or facial pressure."
    },

    # Throat Model Recommendations
    "Pharyngitis": {
        "title": "Possible Pharyngitis Signs Detected",
        "message": "The model identifies inflammation consistent with pharyngitis (sore throat).",
        "advice": "Stay hydrated and rest your throat. If you have severe throat pain, difficulty swallowing, high fever, or symptoms lasting several days, consult a physician."
    },
    "Tonsillitis": {
        "title": "Possible Tonsillitis Signs Detected",
        "message": "The AI model identifies visual indicators of tonsillar inflammation or exudate.",
        "advice": "Seek medical evaluation from a doctor to differentiate between viral and bacterial causes, especially if accompanied by fever, swollen lymph nodes, or difficulty swallowing."
    },

    # Universal Normal Class Recommendation
    "Normal": {
        "title": "Normal Appearance Predicted",
        "message": "The medical image was classified as Normal by the AI model.",
        "advice": "No significant anatomical abnormality was detected by the algorithm. However, if you are experiencing pain, discharge, discomfort, fever, or other symptoms, always seek evaluation by a qualified healthcare professional."
    }
}

DEFAULT_RECOMMENDATION = {
    "title": "General Educational Information",
    "message": "The image has been analyzed by the selected AI classification model.",
    "advice": "This automated analysis is intended for educational purposes only. If you have any health concerns, please consult a qualified healthcare provider."
}


def get_recommendation(predicted_class):
    """
    Retrieve educational recommendation for a predicted condition.
    
    Parameters:
        predicted_class (str): Name of the class predicted by the ML model.
        
    Returns:
        dict: Containing 'title', 'message', and 'advice'.
    """
    return RECOMMENDATIONS.get(predicted_class, DEFAULT_RECOMMENDATION)
