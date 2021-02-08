import logging
from metadata_from_json import dztiles_url, artist_and_title
from format_url import image_json
from main import fabulous_picture
from urllib.parse import urljoin


def amend_dz_url(root_url):
    stem = root_url[:-12]
    new_dz_num = "9/{}_{}.jpg"
    new_dz_url = urljoin(stem, new_dz_num)
    return new_dz_url
    

def save_pic(artsy_url):
    bootstrap = image_json(artsy_url)
    jpeg_label = artist_and_title(bootstrap)
    root_url = dztiles_url(bootstrap)
    if root_url:
        try:
            fabulous_picture(root_url, jpeg_label)
        except SystemError as e:
            logging.error(f"attempting to fetch: {artsy_url}")
            logging.error(f"artwork name: {jpeg_label}")
            try:
                amended_dz_url = amend_dz_url(root_url)
                fabulous_picture(amended_dz_url, jpeg_label)
            except:
                raise e
    else:
        logging.warning(f"{jpeg_label} has no high resolution version. Skipping")
        
    
# save_pic("https://www.artsy.net/artwork/david-wojnarowicz-arthur-rimbaud-in-new-york-diner-2")
# save_pic("https://www.artsy.net/artwork/bert-stern-pirelli-calendar-by-bert-stern")  # no dztiles
# save_pic("https://www.artsy.net/artwork/salvador-dali-madonne")

# these 3 have aspect ratios of 0.99 or 1, and dztiles/9
# save_pic("https://www.artsy.net/artwork/joel-peter-witkin-carrot-cake-number-1")
# save_pic("https://www.artsy.net/artwork/stanley-whitney-untitled-449")
# save_pic("https://www.artsy.net/artwork/georges-mazilu-portrait-de-femme")


# print(amend_dz_url("https://d32dm0rphc51dk.cloudfront.net/naV_9uqzYITVYviI1V2iHA/dztiles/10/{}_{}.jpg"))