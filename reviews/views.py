import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Review
from textblob import TextBlob
from django.utils import timezone

@csrf_exempt
def review_list_create(request):

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            review_text = body.get("review", "").strip()

            if not review_text:
                return JsonResponse({"error": "Review cannot be empty"}, status=400)

            # --- NLP SENTIMENT (basic but valid library usage) ---
            polarity = TextBlob(review_text).sentiment.polarity

            if polarity > 0:
                sentiment = "Positive"
            elif polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            # --- SIMPLE CATEGORY RULE (you can improve later) ---
            text_lower = review_text.lower()

            if "wait" in text_lower or "delay" in text_lower:
                category = "Waiting Time"
            elif "service" in text_lower or "waiter" in text_lower:
                category = "Service"
            elif "clean" in text_lower:
                category = "Cleanliness"
            elif "price" in text_lower:
                category = "Pricing"
            elif "music" in text_lower or "ambience" in text_lower:
                category = "Atmosphere"
            else:
                category = "Food Quality"

            # --- SAVE TO DB ---
            review_obj = Review.objects.create(
                text=review_text,
                sentiment=sentiment,
                category=category,
                
            )

            return JsonResponse({
                "id": review_obj.id,
                "review": review_text,
                "sentiment": sentiment,
                "category": category
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "GET not supported"}, status=405)