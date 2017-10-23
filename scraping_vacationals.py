#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing libraries
from bs4 import BeautifulSoup
import urllib
import os
import urllib.request

def get_name(content):
    info_div = content.find('div', { "class" : "info poi-info dp" })
    name_div = info_div.find('div', {"class": "title"})
    if (name_div == None):
        name = ""
    else:
        name = name_div.select_one("span").text.replace(",", "")

    return name

def info(content):
     # Extract name, url
    info_div = content.find('div', { "class" : "info poi-info dp" })
    name_div = info_div.find('div', {"class": "title"})
    if (name_div == None):
        name = ""
    else:
        name = name_div.select_one("span").text.replace(",", "")
        print(name)
    
     # Extract average_rating
    average_rating_div = info_div.find('div', { "class" : "prw_rup prw_common_location_rating_simple" })
    average_rating = extract_rating(average_rating_div)
    
    # Extract total_reviews_received, reviews_url 
    reviews_div = info_div.find('div', { "class" : "reviews" })
    reviews_count = reviews_div.find('a', { "class" : "review-count" })
    if (reviews_count == None):
        total_reviews_received = "0"
    else:
        total_reviews_received = reviews_count.text.split(' ')[0].replace(",","")
        print(total_reviews_received)
        reviews_url = reviews_count['href']
        reviews_url = trip_advisor_url + reviews_url
       
    # Extract Address
    address_div = info_div.find('div', { "class" : "address" })
    if (address_div == None):
        address = ""
    else:
        address = address_div.text
        address = address.replace(",", "")
           
            
    # Extract current_price_per_night
    price_div = content.find('div', { "class" : "price autoResize  " })
    if (price_div == None):
        current_price_per_night = ""
    else:
        current_price_per_night = price_div.text
   
    return name, address, current_price_per_night, average_rating, total_reviews_received, reviews_url

def extract_rating(rating_div):
    if (rating_div == None):
        rating = ""
    else: 
        if (rating_div.find("span", {"class": "ui_bubble_rating bubble_50"}) != None):
            rating = 5
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_45"}) != None):
            rating = 4.5
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_40"}) != None):
            rating = 4
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_35"}) != None):
            rating = 3.5
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_30"}) != None):
            rating = 3
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_25"}) != None):
            rating = 2.5
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_20"}) != None):
            rating = 2
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_15"}) != None):
            rating = 1.5
        elif (rating_div.find("span", {"class": "ui_bubble_rating bubble_10"}) != None):
            rating = 1
        else:
            rating = ""
    return rating

base_path =  os.path.dirname(os.path.abspath('__file__'))   


file = open(os.path.expanduser(r""+base_path+"/datasets/Finland_Vacationals_Reviews.csv"), "wb")
file.write(b"name,current_price_per_night,average_rating,total_reviews_received,address,lat,lng,reviewer_nationality,rating,rating_date,review_title,review,tags"+ b"\n")
        
trip_advisor_url = "https://www.tripadvisor.com"
WebSites = [
    trip_advisor_url + "/Search?geo=189896&q=summer+holidays&uiOrigin=trip_search_Hotels&searchSessionId=BD1E1BA89C669B256767DB5A643A0FF21508068582914ssid#&ssrc=A&o=0"
    ]
# looping through each site until it hits a break
for page_url in WebSites:
    page_source = urllib.request.urlopen(page_url).read()
    soup = BeautifulSoup(page_source, "lxml")
    divs = soup.find_all('div', {"class": "result LODGING"})
    
    for content in divs:
        
        name, address, current_price_per_night, average_rating, total_reviews_received, reviews_url = info(content)
        if (total_reviews_received == "0"):
            continue
        
        content_page_source = urllib.request.urlopen(reviews_url).read()
        content_soup = BeautifulSoup(content_page_source, "lxml")
        page = 1 
        while True:       
            # Extract Lat, Lng
            lat = lng = ""
            all_script  = content_soup.find_all("script", {"src":False})
            keys = ['lat', 'lng']
            for script in all_script:
                all_value =  script.string   
                if (all_value == None):
                    continue
                for line in all_value.splitlines():
                    if line.split(':')[0].strip() in keys:
                        if (line.split(':')[0].strip() == keys[0]):
                            lat = line.split(':')[1].strip()
                        else:
                            lng = line.split(':')[1].strip()
            lat = lat.replace(",", "")
            lng = lng.replace(",", "")
            
             # Extract Tags
            tags_div = content_soup.find('div', { "class" : "ui_tagcloud_group easyClear"})
            if (tags_div == None):
                tags = ""
            else:
                tags_span = tags_div.find_all("span", {"class": "ui_tagcloud fl "})
                if (tags_span == None):
                    tags = ""
                else:
                    tags = ""
                    for t_span in tags_span:
                        tags = tags + ":"+ t_span["data-content"]
                    if (len(tags) > 1):
                        tags = tags[1:]
           
            reviews = content_soup.find_all('div', {"class": "review-container"})
            
            # Loop through all reviews aavailable on page
            for review in reviews:
                # Extract reviewer_name
                reviewer_name_div = review.find('div', {"class": "username mo"})
                if (reviewer_name_div == None):
                    reviewer_name = ""
                else:
                    reviewer_name = reviewer_name_div.find("span", {"class": "expand_inline scrname"}).text
                    reviewer_name = reviewer_name.replace(",", " ")
                    
                # Extract reviewer_nationality
                reviewer_location_div = review.find('div', {"class": "location"})
                if (reviewer_location_div == None):
                    reviewer_nationality = ""
                else:
                    reviewer_nationality = reviewer_location_div.find("span", {"class": "expand_inline userLocation"}).text
                    reviewer_nationality = reviewer_nationality.replace(",", " ")
                    
                    
                # Extract rating_given_by_reviewer, review_date
                rating_div = review.find("div", {"class": "rating reviewItemInline"})
                rating = extract_rating(rating_div)
                   
                review_date_span = rating_div.find("span", {"class": "ratingDate relativeDate"})
                if (review_date_span != None):
                    review_date = review_date_span["title"].replace(",","")
                else:
                    review_date = ""
                    
                # Extract review_title, 
                review_title_div = review.find("div", {"class": "quote"})
                if (review_title_div != None):
                    review_title_span = review_title_div.find("span", {"class": "noQuotes"})
                    if (review_title_span != None):
                        review_title = review_title_span.text
                    else:
                        review_title = ""
                else:
                    review_title = ""
                review_title = review_title.replace(",", " ")
                
                # Extract review
                review_div = review.find("div", {"class": "prw_rup prw_reviews_text_summary_hsx"})
                if (review_div == None):
                    review = ""
                else:
                    partial_review = review_div.find("p", {"class": "partial_entry"})
                    if (partial_review == None):
                        review = ""
                    else:
                        review = partial_review.text[:-6]
                review = review.replace(",", " ")
                review = review.replace("\n", " ")
                
                
                 # Add Record
                record = str(name) + "," + str(current_price_per_night) + "," + str(average_rating) + "," + str(total_reviews_received) + "," + str(address) + "," + str(lat) + "," + str(lng) + "," + str(reviewer_nationality) + "," + str(rating) + "," +str(review_date) + "," +str(review_title) + "," + str(review) + "," + str(tags)               
                
                file.write(bytes(record, encoding="ascii", errors='ignore')  + b"\n")
  
            # Extract pagination url 
            count = float(total_reviews_received)/10
            if (count > 250):
                count = 250
            pagination_div = content_soup.find('div', { "class" : "unified pagination north_star "})
            if (pagination_div == None):
                break
            page_div = content_soup.find('div', { "class" : "pageNumbers"})
            if (page_div == None):
                break
            pagination_spans = page_div.find_all('span', { "class" : "pageNum taLnk " })
            if (pagination_spans == None):
                break
            next_url = ""
            if ((page < count) & (len(pagination_spans) > 3)):
                page = page + 2
                next_url = pagination_spans[3]['data-href'] 
                next_url = trip_advisor_url + next_url
                hotel_page_source = urllib.request.urlopen(next_url).read()
                hotel_soup = BeautifulSoup(hotel_page_source, "lxml")
            else:
                break    
file.close()