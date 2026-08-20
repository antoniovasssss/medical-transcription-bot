# Medical Transcription Bot

This project reads medical transcriptions from a CSV file, uses the OpenAI API
to extract structured information, and saves the successful results to a new
CSV file.

## What It Extracts

For each transcription, the script requests:

- Patient age
- Recommended treatment or procedure
- A suggested ICD-10-CM code

The source medical specialty and full transcription are also retained in the
output file.

> [!IMPORTANT]
> ICD-10-CM codes produced by the model are suggestions only. They must be
> reviewed and verified by a qualified medical coding professional before use.

## Prerequisites

- Python 3
- An OpenAI API key

Install the required Python packages:

```powershell
python -m pip install openai pandas python-dotenv
```

## Configuration

Create a `.env` file in the project root and add your API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

Do not commit `.env` files or API keys to source control.

## Input Data

The script reads [data/transcriptions.csv](data/transcriptions.csv). It expects
these columns:

| Column | Description |
| --- | --- |
| `medical_specialty` | The clinical specialty associated with the transcription. |
| `transcription` | The medical transcription text to process. |

Example:

```csv
medical_specialty,transcription
Cardiology,"A 65-year-old male presents with chest pain on exertion."
```

## Run the Script

From the project root, run:

```powershell
python app.py
```

The script prints progress for each record. If a record fails to process, it
prints the error and continues with the remaining records.

## Output Data

Successful records are written to
[data/structured_medical_data.csv](data/structured_medical_data.csv). The file
contains these fields:

| Column | Description |
| --- | --- |
| `Age` | Extracted patient age. |
| `Recommended Treatment/Procedure` | Extracted recommended treatment or procedure. |
| `ICD Code` | Suggested ICD-10-CM code associated with the condition, treatment, or procedure. |
| `Medical Specialty` | The source `medical_specialty` value. |
| `Transcription` | The original source transcription. |

## Data Handling

Medical transcriptions may contain sensitive health information. Use only data
you are authorized to process, follow your organisation's privacy and security
requirements, and confirm that sending data to the selected API provider is
appropriate for your use case.