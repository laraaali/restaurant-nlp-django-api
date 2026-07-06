**Restaurant NLP Django API**
**Project Overview**
This project is a Django-based REST API that analyzes customer reviews for a restaurant using Natural Language Processing (NLP).
It processes reviews, determines sentiment, and classifies each review into a category such as food, service, or pricing.
The system also includes a Django management command to import and analyze a dataset of restaurant reviews.

**Tech Stack**
Python 3.12+
Django 5+
Django REST Framework
TextBlob (NLP library)

**Installation**
**1. Clone the repository**
    git clone https://github.com/laraaali/restaurant-nlp-django-api.git
    cd restaurant-nlp-django-api
**2. Create virtual environment (optional but recommended)**
    python -m venv venv
    venv\Scripts\activate   # Windows
**3. Install dependencies**
    pip install django djangorestframework textblob
**4. Run migrations**
     python manage.py migrate

**Operations**

## Import Dataset

Import the provided restaurant reviews into the database:

```bash
python manage.py import_reviews feedback-abudhabi-50-gpt.txt
```

## Verify Imported Data

Open the Django shell:

```bash
python manage.py shell
```

Run the following commands to verify the imported reviews:

```python
from reviews.models import Review

# Total number of reviews
Review.objects.count()

# View the first 5 reviews
Review.objects.all()[:5]

# View a specific review (example: 13th review)
Review.objects.all()[12]

# Display the review text, sentiment, and category
Review.objects.values("text", "sentiment", "category")[:5]
```

To remove all reviews from the database (optional):

```python
Review.objects.all().delete()
```

Exit the Django shell:

```python
exit()
```

**Run the Application**

**Start the Django development server:**

```bash
python manage.py runserver
```

**The API will be available at:**

```text
http://127.0.0.1:8000/
```

## Example API Request

**Use PowerShell to submit a new customer review:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/reviews/" `
-Method POST `
-ContentType "application/json" `
-Body '{"review":"The food was amazing"}'
```

### Example Response

```json
{
  "id": 51,
  "review": "The food was amazing",
  "sentiment": "Positive",
  "category": "Food Quality"
}
```


