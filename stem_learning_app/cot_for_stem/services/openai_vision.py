import base64

from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class ExerciseVisionService:
    """
    Analyse un exercice (image ou PDF) et retourne
    une résolution pédagogique découpée en étapes + QCM.
    """

    @staticmethod
    def analyze_exercise(file_url: str, subject: str = "general"):
        """
        file_url : URL publique ou lien S3 de l'image/PDF
        subject  : maths | physique | svt | francais | anglais
        Pour les sujets de maths, les formulaires doivent être au format Latex.
        """

        prompt = f"""
            Tu es un professeur expert en {subject}.
            
            Analyse le présent dans le document fourni.
            Découpe le document en exercice.
            Pour chaque exercie, Découpe la résolution en étapes pédagogiques successives.
            
            Pour chaque document, retourne STRICTEMENT le JSON suivant:
            
            {{
            "exercise_1":
                [
                    {{
                          "step_number": 1,
                          "objective": "...",
                          "question": "...",
                          "choices": ["A", "B", "C", "D"],
                          "correct_answer": "A",
                          "explanation": "..."
                        }},
                    {{
                          "step_number": 2,
                          "objective": "...",
                          "question": "...",
                          "choices": ["A", "B", "C", "D"],
                          "correct_answer": "A",
                          "explanation": "..."
                        }},
                        
                ],
            "exercise_2":
                [
                    {{
                          "step_number": 1,
                          "objective": "...",
                          "question": "...",
                          "choices": ["A", "B", "C", "D"],
                          "correct_answer": "A",
                          "explanation": "..."
                        }},
                    {{
                          "step_number": 2,
                          "objective": "...",
                          "question": "...",
                          "choices": ["A", "B", "C", "D"],
                          "correct_answer": "A",
                          "explanation": "..."
                        }},
                        
                ],    
                
            }}
            
            Contraintes :
            - Niveau lycée
            - Raisonnement progressif
            - QCM pédagogiques (pas triviaux)
            - Aucun texte hors JSON
        """
        # Path to your image
        image_path = file_url

        # Getting the Base64 string
        base64_image = encode_image(image_path)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    ]
                }
            ],
            max_output_tokens=4800
        )

        return response.output_text
