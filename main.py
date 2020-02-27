import os
import string
from util.attributes_retrieval import get_attrs, get_max_page_for_letter

def main():
    values = []
    for letter in string.ascii_lowercase:
        max_page = get_max_page_for_letter('a')
        for page in range(1, max_page+1):
            values.extend(get_attrs("https://www.world-airport-codes.com/alphabetical/airport-name/{}.html?page={}".format(letter, page)))

    df = pd.DataFrame(np.array(values),
                   columns=['name', 'city', 'country', 'zip_code'])
    df.to_csv('airport.csv', index = False)

if __name__ == '__main__':
    if os.getenv("API_KEY") is None:
        raise Exception("Please specify API_KEY before proceed!")
    main()
