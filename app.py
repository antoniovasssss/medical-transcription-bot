import json
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv


# ---------------------------------------
# 1. Initialize OpenAI client
# ---------------------------------------

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set. Add it to your .env file.")

client = OpenAI(api_key=API_KEY)

# ---------------------------------------
# 2. Load CSV data
# ---------------------------------------

df = pd.read_csv("data/transcriptions.csv")

print("Number of records:", len(df))
print(df.head())


# ---------------------------------------
# 3. Function to process one transcription
# ---------------------------------------

def extract_medical_data(transcription, medical_specialty):
    """
    Extract age, treatment/procedure and ICD code
    from a medical transcription using one OpenAI call.
    """

    messages = [
        {
            "role": "system",
            "content": """
You are a healthcare data extraction assistant.

Extract structured information from the medical transcription.

Return:
1. Patient age
2. Recommended treatment or procedure
3. ICD-10-CM code related to the recommended treatment,
   procedure, or medical condition.

If information is missing, return "Unknown".

The ICD code should be treated as an AI-generated suggestion
and should be verified by a qualified medical coding professional.
"""
        },
        {
            "role": "user",
            "content": f"""
Medical Specialty:
{medical_specialty}

Medical Transcription:
{transcription}

Extract the requested medical information.
"""
        }
    ]

    # ---------------------------------------
    # Function definition
    # ---------------------------------------

    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_medical_data",
                "description": "Extract structured medical information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Age": {
                            "type": "integer",
                            "description": "Patient's age"
                        },
                        "Recommended Treatment/Procedure": {
                            "type": "string",
                            "description": (
                                "Recommended treatment or medical procedure"
                            )
                        },
                        "ICD Code": {
                            "type": "string",
                            "description": (
                                "Suggested ICD-10-CM code related "
                                "to the condition, treatment, or procedure"
                            )
                        }
                    },
                    "required": [
                        "Age",
                        "Recommended Treatment/Procedure",
                        "ICD Code"
                    ]
                }
            }
        }
    ]

    # ---------------------------------------
    # ONE OpenAI API CALL
    # ---------------------------------------

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {
                "name": "extract_medical_data"
            }
        }
    )

    # ---------------------------------------
    # Get function arguments
    # ---------------------------------------

    tool_call = response.choices[0].message.tool_calls[0]

    arguments = tool_call.function.arguments

    return json.loads(arguments)


# ---------------------------------------
# 4. Process the dataset
# ---------------------------------------

processed_data = []

for index, row in df.iterrows():

    print(
        f"Processing record {index + 1}/{len(df)}..."
    )

    try:

        medical_specialty = row["medical_specialty"]
        transcription = row["transcription"]

        # One OpenAI call
        extracted_data = extract_medical_data(
            transcription,
            medical_specialty
        )

        # Add medical specialty
        extracted_data["Medical Specialty"] = medical_specialty

        # Add original transcription
        extracted_data["Transcription"] = transcription

        # Store result
        processed_data.append(extracted_data)

        print(extracted_data)

    except Exception as e:

        print(
            f"Error processing row {index}: {e}"
        )


# ---------------------------------------
# 5. Create structured DataFrame
# ---------------------------------------

df_structured = pd.DataFrame(processed_data)


# ---------------------------------------
# 6. Display final result
# ---------------------------------------

print("\n")
print("=" * 80)
print("FINAL STRUCTURED DATA")
print("=" * 80)

print(df_structured.to_string(index=False))


# ---------------------------------------
# 7. Save results
# ---------------------------------------

output_file = "data/structured_medical_data.csv"

df_structured.to_csv(
    output_file,
    index=False
)

print("\n")
print(f"Results saved to: {output_file}")