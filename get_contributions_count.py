from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import collections

user = "proselotis"
base_url = "https://github.com"




# count how many years the profile has existed by using the years next to contirbution activity
base_request = requests.get(f"{base_url}/{user}")
base_soup = BeautifulSoup(base_request.text, "html.parser")
mydivs = base_soup.find_all("a", {"class": "js-year-link filter-item px-3 mb-2 py-2"})
extended_urls = [year_bracket['href'] for year_bracket in mydivs]

# add the year that we are currently in, as that does not show up 
extended_urls.insert(0,f"/{user}")

# for each year collect the count of contributions for each date 
date2contributions = {}
for extended_url in tqdm(extended_urls): 
    r = requests.get(f"{base_url}{extended_url}")
    soup = BeautifulSoup(r.text, "html.parser")
    for tr in soup.find_all("rect"):
        try:
            date2contributions[tr['data-date']] = int(tr['data-count'])
        except:
            # should just be extra content that is not dates represented in the bottom
            pass


# sort by key
# ordered_date2contributions = collections.OrderedDict(sorted(date2contributions.items()))
# sort by value
ordered_date2contributions = dict(sorted(date2contributions.items(), key=lambda item: item[1],reverse=True))