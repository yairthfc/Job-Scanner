# === REMOTIVE CONFIGURATION ==============
REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"

# === ADZUNA CONFIGURATION ================
ADZUNA_API_URL_TEMPLATE = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
ADZUNA_APP_ID = "35fb2824"
ADZUNA_APP_KEY = "ff638f97d7ed3087a321e069ea4403df"


# === GOONZILE (AIRTABLE) CONFIGURATION ===
GOONZILE_IFRAME_URL = "https://airtable.com/embed/appwewqLk7iUY4azc/shrQBuWjXd0YgPqV6/tblnk93ouV3B2ce9b?viewControls=on"
GOONZILE_IFRAME_URL_START = 'urlWithParams: '
GOONZILE_IFRAME_URL_END = 'earlyPrefetchSpan:'
GOONZILE_BASE_HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Airtable-Accept-Msgpack': 'true',
    'X-Airtable-Inter-Service-Client': 'webClient',
    'X-Early-Prefetch': 'true',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Time-Zone': 'Europe/London',
    'X-User-Locale': 'en'
}

# === COUNTRY NAME → ISO CODE MAP =========
country_map = {
    "united states": "us", "usa": "us", "us": "us", "america": "us",
    "united kingdom": "gb", "uk": "gb", "great britain": "gb", "england": "gb", "britain": "gb",
    "australia": "au", "au": "au",
    "austria": "at", "at": "at",
    "belgium": "be", "be": "be",
    "brazil": "br", "br": "br", "brasil": "br",
    "canada": "ca", "ca": "ca",
    "france": "fr", "fr": "fr",
    "germany": "de", "de": "de", "deutschland": "de",
    "india": "in", "in": "in",
    "italy": "it", "it": "it", "italia": "it",
    "mexico": "mx", "mx": "mx", "méxico": "mx",
    "netherlands": "nl", "nl": "nl", "holland": "nl",
    "new zealand": "nz", "nz": "nz",
    "poland": "pl", "pl": "pl", "polska": "pl",
    "south africa": "za", "za": "za",
    "spain": "es", "es": "es", "españa": "es",
    "switzerland": "ch", "ch": "ch", "schweiz": "ch"
}

# === ISRAEL CITY → AIRTABLE ID MAP =======
normalized_cites_map = {
    "airport city": ["selv8I5XnhAmg8Wy4"],
    "ashdod": ["selpRdUllK6Ardz2x"],
    "ashkelon": ["selKT8gWZL6nbCdbL"],
    "beer sheva": ["sel6iPNei78rcdNNq"],
    "beit haemek": ["el9hEVL0xLnulE0R"],
    "beit yannai": ["selZSPsG3ouh61hRS"],
    "binyamina": ["selCTy2k39e9Ae0qw"],
    "bnei brak": ["selugunpolndT3W8A"],
    "caesarea": ["seliz5TkwObwaNBun"],
    "givatayim": ["selsx44AlHaXzc4rr"],
    "haifa": ["sel4tuz1iIKQlCuET", "seltGxZP4wSvszcGx"],
    "herzliya": ["selk1UMxQtJUnu7ZB"],
    "hod hasharon": ["selZRGfMgtharKouc"],
    "holon": ["selKKJonXQJsCCxQh"],
    "yiftah": ["selogvHiZkN5UnHR9"],
    "israel - central": ["selDqPZe70uXQnaYY", "sel0Klfcj1N11kaGi", "self85GfymLj0ZPrG"],
    "israel - north": ["selliTzBB01LNe9SF"],
    "israel - remote": ["selLOMlwNCzC3iY48"],
    "jerusalem": ["selcNDUysXHclXKhC"],
    "karmiel": ["selfMUyRq9x5qUawQ"],
    "kfar saba": ["selk5KbQBLw1jSf15"],
    "kiryat gat": ["sel2Ufkbod09h0kqP"],
    "kiryat ono": ["selUjlaekJWPPCci9"],
    "lod": ["selwALjRNTGXxhyIP"],
    "magal": ["selLBC2pkbfroRBfB"],
    "migdal haemek": ["selJNXzmuhfZFEglQ"],
    "modi'in": ["selWuuYSWPetAeEaU"],
    "ness ziona": ["selBja6yl09FuBF34"],
    "netanya": ["selzEafnLfkG24XSX"],
    "or yehuda": ["selZ2FIWdhLFRSqHT"],
    "petach tikva": ["selCClpz2B5VWMweT"],
    "ra'anana": ["selovb23uxpfDK2Mw"],
    "ramat gan": ["selNqSmIKl4jB4FdT"],
    "ramat hasharon": ["selMM5CqIL7sPD7aS"],
    "rehovot": ["seltglDY90udBpCO4"],
    "rishon lezion": ["selSBGAD2FvxeVaFq"],
    "rosh haayin": ["selaQ4hxxYSlf7tk1"],
    "shoham": ["selIP1CLsbvY9y16X"],
    "tel aviv": ["selEVE30mDzRv5jFN", "selXkSXbXUjNNJUgt"],
    "tel hai": ["selllM0fP6KIQmLAJ"],
    "yavne": ["selGwaf1r7pVKjqo1"],
    "yokne'am": ["selmgV10E0kALV9ev"]
}
