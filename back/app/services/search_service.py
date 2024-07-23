###Version 4
#from app.models.cafe_model import Cafe                 
#from typing import List, Dict, Any
#import re 
#import unicodedata

# Dictionnaire de stopwords
#import nltk
#from nltk.corpus import stopwords
#nltk.download('stopwords')
#french_stopwords= set(stopwords.words('french'))
#english_stopwords = set(stopwords.words('english'))
#print(french_stopwords)
#print(english_stopwords)


# Fonction pour ignorer les stop words dans la recherche 
#def filter_stopwords(phrase: str) -> str:
#    #separation = r"\b\w+'|\w+"                            # conserve l'apostrophe lors de la séparation (sans nltk)
#    separation = r"\b\w+(?=')|(?<=')\w+|\b\w+"             # ne conserve pas l'apostrophe lors de la séparation (avec nltk)
#    phrase_seperated = re.findall(separation, phrase)      # ceci renvoie un tableau
#    #print(phrase_seperated)
#    phrase_filtered = [word for word in phrase_seperated if word.lower() not in french_stopwords]
#    #print(phrase_filtered)
#    new_phrase = ' '.join(phrase_filtered)
#    return new_phrase

#def normalize_search(phrase:str) -> str:
#    #normalized_text = unicode.unicode(phrase)     # autre méthode
#    phrase = unicodedata.normalize('NFKD', phrase)
#    normalized_text = phrase.encode('ascii', 'ignore').decode('ascii')
#    return normalized_text


#async def search(query: str, **filters) -> Dict[str, List[Any]]:      

#    query_filtered = filter_stopwords(query)
#    print(query)
#    print(query_filtered)


#    regex_pattern = {"$regex": query_filtered, "$options": "i"}
                                                                
#    for key in ['is_open', 'in_stock']:                     
#        if key in filters:
#            if filters[key].lower() == 'true':              
#                filters[key] = True
#            elif filters[key].lower() == 'false':
#                filters[key] = False


#    combined_query =  {
#        "$or":[  
#            {"name": regex_pattern},
#            {"menu_items": {"$elemMatch": {"name": regex_pattern}}}, 
#            {"menu_items": {"$elemMatch": {"tags": regex_pattern}}},
#    
#        ]
#    }
    
#    combined_query.update(filters)      # rajoute le précédent aux filters
#    matching_cafes_full = await Cafe.find(combined_query).to_list()    


#    matching_cafes_and_items = []                       
#    for cafe in matching_cafes_full:
#        # filtered_menu_items = [item for item in cafe.menu_items if query.lower() in item.name.lower()]
#        filtered_menu_items = [item for item in cafe.menu_items if query.lower() in item.name.lower() or any(query.lower() in tag.lower() for tag in item.tags)]
        
#        cafe_dict = {                                 
#            "_id": str(cafe.id), 
#            "cafe_id": str(cafe.cafe_id),
#            "name": cafe.name,
#            "slug": cafe.slug,
#            "description": cafe.description,
#            "image_url": cafe.image_url,
#            "faculty": cafe.faculty,
#            "is_open": cafe.is_open,
#            "status_message": cafe.status_message,
#            "opening_hours": cafe.opening_hours,
#            "location": cafe.location,
#            "contact": cafe.contact,
#            "social_media": cafe.social_media,
#            "payment_methods": cafe.payment_methods,
#            "additional_info": cafe.additional_info,
#            "menu_items": filtered_menu_items            
#        }
#        matching_cafes_and_items.append(cafe_dict)        

#    return matching_cafes_and_items                     
    



###Version 5 (Daniela)
from app.models.cafe_model import Cafe
from typing import List, Dict, Any
import re
import unicodedata
import Levenshtein

# Dictionnaire de stopwords
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
french_stopwords= set(stopwords.words('french'))
#english_stopwords = set(stopwords.words('english'))
#print(french_stopwords)
#print(english_stopwords)


# Fonction permettant d'ignorer les mots vides (stop words) dans la recherche 
def filter_stopwords(phrase: str) -> str:
    #separation = r"\b\w+'|\w+"                            # conserve l'apostrophe lors de la séparation (sans nltk)
    separation = r"\b\w+(?=')|(?<=')\w+|\b\w+"             # ne conserve pas l'apostrophe lors de la séparation (avec nltk)
    phrase_seperated = re.findall(separation, phrase)      # renvoie un tableau
    phrase_filtered = [word for word in phrase_seperated if word.lower() not in french_stopwords]
    new_phrase = ' '.join(phrase_filtered)
    return new_phrase

# Fonction permettant de normaliser les mots dans la recherche
def normalize_search(phrase:str) -> str:
    phrase = unicodedata.normalize('NFKD', phrase)
    normalized_text = phrase.encode('ascii', 'ignore').decode('ascii').lower()
    return normalized_text

# Fonction permettant de normaliser le score de similarité en utilisant Levenshtein distance
def similarity(str1,str2):
    if len(str1) != 0 and len(str2) != 0:
        return 1 - ( Levenshtein.distance(str1, str2) / min(len(str1),len(str2)))
 

async def search(query: str, **filters) -> Dict[str, List[Any]]:
    query_filtered = filter_stopwords(query)
    #normalized_query = normalize_search(query_filtered)         # déjà normaliser par le front end
    print(query)
    print(query_filtered)

    # Filtres supplémentaires
    for key in ['is_open', 'in_stock']:
        if key in filters:
            if filters[key].lower() == 'true':
                filters[key] = True
            elif filters[key].lower() == 'false':
                filters[key] = False
 

    all_cafes = await Cafe.find().to_list()            # liste de tous les cafés
    query_tokenized = query_filtered.split(' ') 
    #print(query_tokenized)
    similarity_score = 0.7              # modifier le score de similarité au besoin


    if query_filtered == '':            # Cas: l'utilisateur entre un string vide
        matching_cafes_full = all_cafes
    
    else:
        # Recherche de cafés par leur nom
        matching_cafes_by_name = [
    
            cafe for cafe in all_cafes 

            if (
                (name_filtered := filter_stopwords(cafe.name),         # définir les variables
                name_normalized := normalize_search(name_filtered),
                name_tokenized := name_normalized.split(' ')
                )

                and any(query_token in name_normalized for query_token in query_tokenized)   # si c'est une phrase au moins un mot match
                or any(similarity(query_token, name_token) >= similarity_score for query_token in query_tokenized for name_token in name_tokenized)
            )
            #and all(cafe.get(attr) == value for attr, value in filters.items())            # rajoute les filtres comme condition
            ]
    

        # Recherche de cafés par les items du menu 
        matching_cafes_by_menu_item = [

            cafe for cafe in all_cafes 

            if (
                any(
                    (item_name_normalized := normalize_search(item.name),
                    item_name_tokenized := item_name_normalized.split(' '))
              
                    and any(query_token in item_name_normalized for query_token in query_tokenized)            # match le nom de l'item
                    or any(similarity(query_token, item_name_token) >= similarity_score for query_token in query_tokenized for item_name_token
                        in item_name_tokenized)

                    for item in cafe.menu_items
                )        
            )   
            #and all(cafe.get(attr) == value for attr, value in filters.items())            # rajoute les filtres comme condition
            and cafe not in matching_cafes_by_name 
            ]
        

        # Recherche des cafés par les tags du menu
        matching_cafes_by_tag = [

            cafe for cafe in all_cafes

            if(
                any(
                    (item_tag_normalized := list(map(normalize_search, item.tags)))          # normalsier les tags

                    and any(query_token in item_tag_normalized for query_token in query_tokenized)             # match le tag
                    or any(similarity(query_token, tag_token) >= similarity_score for query_token in query_tokenized for tag_token in 
                        item_tag_normalized)
                
                    for item in cafe.menu_items
                )

            )
            #and all(cafe.get(attr) == value for attr, value in filters.items())            # rajoute les filtres comme condition
            ]
        
        matching_cafes_full = matching_cafes_by_name + matching_cafes_by_menu_item + matching_cafes_by_tag     # joindre les listes ensemble

    
    

    matching_cafes_and_items = []
    for cafe in matching_cafes_full:
        filtered_menu_items = [
            item for item in cafe.menu_items
            if query_filtered.lower() in item.name.lower() or any(query_filtered.lower() in tag.lower() for tag in item.tags)
        ]
        
        cafe_dict = {
            "_id": str(cafe.id),
            "cafe_id": str(cafe.cafe_id),
            "name": cafe.name,
            "slug": cafe.slug,
            "description": cafe.description,
            "logo_url": cafe.logo_url,
            "image_url": cafe.image_url,
            "affiliation": cafe.affiliation,
            "is_open": cafe.is_open,
            "status_message": cafe.status_message,
            "opening_hours": cafe.opening_hours,
            "location": cafe.location,
            "contact": cafe.contact,
            "social_media": cafe.social_media,
            "payment_methods": cafe.payment_methods,
            "additional_info": cafe.additional_info,
            "menu_items": filtered_menu_items
        }
        matching_cafes_and_items.append(cafe_dict)

    return matching_cafes_and_items


# Combining the search for cafes by their name and by menu items
    #combined_query = {
    #    "$or": [
    #        {"name": regex_pattern},
    #        {"menu_items": {"$elemMatch": {"name": regex_pattern}}},
    #        {"menu_items": {"$elemMatch": {"tags": regex_pattern}}}
    #    ]
    #}
    #combined_query.update(filters)



 #global matching_cafes_full
    #matching_cafes_full = []                # liste vide pour stocker les cafés correspondant à la recherche
    #matching_cafes_full.append(filters)     # rajouter les filtres supplémentaires
    #for cafes in await Cafe.find().to_list():
    #cafe_name = cafes.name   
    #name_filtered = filter_stopwords(cafe_name)
    #name_normalized = normalize_search(name_filtered)
    #    #print(cafe_name)
    #print(name_normalized) 
    #    if query_filtered in name_normalized:
    #       #print(similarity(query_filtered,name_normalized))
    #       matching_cafes_full.append(cafes)


    #for cafes in await Cafe.find().to_list():
    #    for item in cafes.menu_items:
    #        #print(item.name)
    #        #print(item.tags)
    #        item_name = item.name
    #        item_tag = item.tags
    #        item_tag_normalized = list(map(normalize_search, item_tag)) 
    #        #print(tag_normalized)
    #        if query_filtered in normalize_search(item.name) or query_filtered in item_tag_normalized:
    #            if cafes not in matching_cafes_full:
    #                matching_cafes_full.append(cafes)