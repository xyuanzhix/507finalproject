import json
CACHE_FILENAME = "cache.json"
if __name__ == '__main__':
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    print(cache_dict)