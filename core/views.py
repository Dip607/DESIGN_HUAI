from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageUploadForm
from .models import UploadedImage
from .utils import get_dominant_colors, get_image_labels, search_pixabay_images, search_freepik_resources,  fetch_pinterest_images
import openai
from django.conf import settings
import google.generativeai as genai
import requests

def poster_generator(request):
    prompt = request.POST.get("prompt", "")

    headers = {
        "Authorization": "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",
        "HTTP-Referer": "http://127.0.0.1:8000",  # important for free tier
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # or try openai/gpt-3.5-turbo
        "messages": [
            {
                "role": "system",
                "content": "You are a poster layout generator. Return only the layout idea or plan, no extra info."
            },
            {
                "role": "user",
                "content": f"Generate a creative tech poster plan for: {prompt}"
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        response_data = response.json()
        if "choices" in response_data:
           layout = response_data["choices"][0]["message"]["content"]
        else:
           layout = f"❌ Error: {response_data.get('error', 'No choices in response')}\n\nFull Response: {response_data}"
    except Exception as e:
        layout = f"❌ Error: {str(e)}"

    return render(request, "core/poster_result.html", {"prompt": prompt, "layout": layout})

def style_search(request):
    style = request.GET.get('style', '')
    pixabay = search_pixabay_images(style, num_results=8)
    freepik = search_freepik_resources(style, num_results=8)
    pinterest = fetch_pinterest_images(style, max_images=8)

    all_images = pixabay + freepik + pinterest

    # Optional: AI filter to re-rank by matching labels
    filtered_images = []
    for img in all_images:
        try:
            labels = get_image_labels(img['image'])
            if any(style.lower() in label.lower() for label in labels):
                filtered_images.append(img)
        except Exception:
            continue

    return render(request, 'core/poster_result.html', {
        'style': style,
        'images': filtered_images or all_images,
    })

def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            # Extract colors and labels
            colors = get_dominant_colors(image_path)
            labels = get_image_labels(image_path)

            # Save extracted features
            uploaded_image.dominant_colors = colors
            uploaded_image.labels = ", ".join(labels)
            uploaded_image.save()

            return redirect('results', pk=uploaded_image.pk)
    else:
        form = ImageUploadForm()
    
    return render(request, 'core/home.html', {'form': form})


def results(request, pk):
    image = get_object_or_404(UploadedImage, pk=pk)

    # Step 1: Extract keywords from labels
    keywords = [kw.strip() for kw in image.labels.split(",")][:2]
    search_query = " ".join(keywords)  # This will be used in all three APIs

    # Step 2: Fetch design inspirations from all sources
    pixabay = search_pixabay_images(search_query, num_results=6)
    freepik = search_freepik_resources(search_query, num_results=6)
    pinterest = fetch_pinterest_images(search_query, max_images=6)

    # Step 3: Combine all inspirations
    inspiration_images = pixabay + freepik + pinterest

    return render(request, 'core/results.html', {
        'image': image,
        'inspiration_images': inspiration_images
    })