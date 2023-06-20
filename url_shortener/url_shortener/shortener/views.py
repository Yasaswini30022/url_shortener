import base64
from django.shortcuts import render, redirect
from .models import ShortenedURL

SHORT_CODE_LENGTH = 6  # Specify the desired length of the short code

def home(request):
    if request.method == 'POST':
        long_url = request.POST['long_url']
        
        try:
            shortened_url = ShortenedURL.objects.get(long_url=long_url)
            return render(request, 'shortener/home.html', {'shortened_url': shortened_url})
        except ShortenedURL.DoesNotExist:
            shortened_url = ShortenedURL(long_url=long_url)
            shortened_url.save()
    
            short_code = generate_short_code(shortened_url.id)
            shortened_url.short_code = short_code
            shortened_url.save()
    
            return render(request, 'shortener/home.html', {'shortened_url': shortened_url})

    return render(request, 'shortener/home.html')


def generate_short_code(number):
    """
    Generate a short code of a specific length from a number using Base64 encoding.
    """
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    short_code = ""
    while number > 0:
        number, remainder = divmod(number, 64)
        short_code = base64_chars[remainder] + short_code
    
    # Truncate or pad the short code to the desired length
    if len(short_code) < SHORT_CODE_LENGTH:
        short_code = short_code.ljust(SHORT_CODE_LENGTH, base64_chars[0])
    elif len(short_code) > SHORT_CODE_LENGTH:
        short_code = short_code[:SHORT_CODE_LENGTH]
    
    return short_code


def redirect_to_long_url(request, short_code):
    try:
        shortened_url = ShortenedURL.objects.get(short_code=short_code)
        return redirect(shortened_url.long_url)
    except ShortenedURL.DoesNotExist:
        return render(request, 'shortener/not_found.html')


def url_list(request):
    urls = ShortenedURL.objects.all()
    return render(request, 'shortener/url_list.html', {'urls': urls})
