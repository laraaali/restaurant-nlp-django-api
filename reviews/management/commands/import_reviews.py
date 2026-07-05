from django.core.management.base import BaseCommand
from reviews.models import Review
from textblob import TextBlob


class Command(BaseCommand):
    help = "Import reviews from text file with sentiment analysis"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]

        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        reviews = []
        current = ""

        # -----------------------------
        # Parse reviews
        # -----------------------------
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line[0].isdigit() and "." in line[:5]:
                if current:
                    reviews.append(current.strip())
                current = line.split(".", 1)[1].strip()
            else:
                current += " " + line

        if current:
            reviews.append(current.strip())

        # -----------------------------
        # NLP + Import
        # -----------------------------
        count = 0

        for review_text in reviews:

            analysis = TextBlob(review_text).sentiment
            polarity = analysis.polarity

            # sentiment
            if polarity > 0:
                sentiment = "Positive"
            elif polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            # category (simple rule-based NLP)
            text = review_text.lower()

            if "service" in text:
                category = "Service"
            elif "food" in text or "taste" in text:
                category = "Food"
            elif "price" in text or "expensive" in text:
                category = "Price"
            elif "ambience" in text or "interior" in text:
                category = "Ambience"
            else:
                category = "General"

            # avoid duplicates
            if not Review.objects.filter(text=review_text).exists():

                Review.objects.create(
                    text=review_text,
                    sentiment=sentiment,
                    category=category
                )

                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Imported {count} reviews with sentiment + category")
        )