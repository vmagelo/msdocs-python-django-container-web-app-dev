import uuid
import os

from . import mongodb

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from bson import ObjectId

# Create your views here.

def index(request):
    print('Request for index page received')  

    collection = mongodb.get_collection()
    results_restaurant_cursor = collection.find({"type" : "restaurant"})

    # Get the list of restaurants   
    restaurants_annotated = []
    for record in results_restaurant_cursor:
        # For each restaurant record, get the list of reviews so we can calculate average rating
        print(record.get("name") + ", " + str(record.get("_id")))
        review_count, avg_rating = get_review_stats(str(record.get("_id")))
        new_record = record
        new_record.update({"review_count" : review_count, "avg_rating" : avg_rating, "id" : str(record.get("_id"))})  
        restaurants_annotated.append(new_record)        

    return render(request, 'restaurant_review/index.html', {'restaurants': restaurants_annotated })

def get_review_stats(id):
    collection = mongodb.get_collection()
    review_count = collection.count_documents({"type" : "review", "restaurant" : ObjectId(id)})
    if review_count > 0:
        avg_rating_group = collection.aggregate([{"$match" : {"type" : "review", "restaurant" : ObjectId(id)}}, {"$group" : {"_id" : "$restaurant", "avg_rating" : {"$avg" : "$rating"}}}])
        avg_rating = avg_rating_group.next().get("avg_rating") 
    else:
        avg_rating = 0
    return review_count, avg_rating

def details(request, id):
    collection = mongodb.get_collection()
    print('Request for restaurant details page received')

    cursor = collection.find({"type" : "restaurant", "_id" : ObjectId(id)})
    restaurant = cursor.next()
    if cursor.retrieved != 0:
        review_count, avg_rating = get_review_stats(id)
        restaurant_annotated = restaurant
        restaurant_annotated.update({"review_count" : review_count, "avg_rating" : avg_rating, "id" : str(restaurant.get("_id"))})  
    else:
        raise Http404("Restaurant not found")
    return render(request, 'restaurant_review/details.html', {'restaurant': restaurant_annotated})

def create_restaurant(request):
    print('Request for add restaurant page received')

    return render(request, 'restaurant_review/create_restaurant.html')

def add_restaurant(request):
    try:
        name = request.POST['restaurant_name']
        street_address = request.POST['street_address']
        description = request.POST['description']
        if (name == "" or description == ""):
            raise RequestException()
    except (KeyError, exceptions.RequestException) as e:
        # Redisplay the restaurant entry form.
        messages.add_message(request, messages.INFO, 'Restaurant not added. Include at least a restaurant name and description.')
        return HttpResponseRedirect(reverse('create_restaurant'))  
    else:
        collection = mongodb.get_collection()
        restaurant = mongodb.create_restaurant_record(name, street_address, description)
        id = collection.insert_one(restaurant).inserted_id
                
        return HttpResponseRedirect(reverse('details', args=(id,)))

def add_review(request, id):
    try: 
        restaurant = Restaurant.objects.annotate(avg_rating=Avg('review__rating')).annotate(review_count=Count('review')).get(pk=id)
    except Restaurant.DoesNotExist:
        raise Http404("Restaurant doesn't exist")

    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
        if (user_name == "" or rating == ""):
            raise RequestException()            
    except (KeyError, exceptions.RequestException) as e:
        # Redisplay the details page
        messages.add_message(request, messages.INFO, 'Review not added. Include at least a name and rating for review.')
        return HttpResponseRedirect(reverse('details', args=(id,)))  
    else:

        if 'reviewImage' in request.FILES:
            image_data = request.FILES['reviewImage']
            print("Original image name = " + image_data.name)
            print("File size = " + str(image_data.size))

            if (image_data.size > 2048000):
                messages.add_message(request, messages.INFO, 'Image too big, try again.')
                return HttpResponseRedirect(reverse('details', args=(id,)))  

            # Create client
            azure_credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
            blob_service_client = BlobServiceClient(
                account_url=account_url,
                credential=azure_credential)

            # Get file name to use in database
            image_name = str(uuid.uuid4()) + ".png"
            
            # Create blob client
            blob_client = blob_service_client.get_blob_client(container=os.environ['STORAGE_CONTAINER_NAME'], blob=image_name)
            print("\nUploading to Azure Storage as blob:\n\t" + image_name)

            # Upload file
            with image_data as data:
                blob_client.upload_blob(data)
        else:
            # No image for review
            image_name=None

        review = Review()
        review.restaurant = restaurant
        review.review_date = timezone.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        review.image_name = image_name
        Review.save(review)
                
    return HttpResponseRedirect(reverse('details', args=(id,)))