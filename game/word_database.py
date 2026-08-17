"""Curated bilingual English/Hindi word and category database for IMPOSTER."""

# Each category contains game-friendly words. English and Hindi are kept together
# so the reveal screen can display both languages without changing game logic.
CATEGORY_DATA = {
    "FOOD": ("भोजन", [
        ("PIZZA", "पिज़्ज़ा"), ("BURGER", "बर्गर"), ("SUSHI", "सुशी"),
        ("BIRYANI", "बिरयानी"), ("DOSA", "डोसा"), ("NOODLES", "नूडल्स"),
        ("SANDWICH", "सैंडविच"), ("PASTA", "पास्ता"), ("TACO", "टैको"),
        ("SAMOSA", "समोसा")]),
    "ANIMALS": ("जानवर", [
        ("LION", "शेर"), ("TIGER", "बाघ"), ("ELEPHANT", "हाथी"),
        ("PENGUIN", "पेंगुइन"), ("DOLPHIN", "डॉल्फ़िन"), ("GIRAFFE", "जिराफ़"),
        ("MONKEY", "बंदर"), ("GORILLA", "गोरिल्ला"), ("CROCODILE", "मगरमच्छ"),
        ("KANGAROO", "कंगारू")]),
    "FRUITS": ("फल", [
        ("APPLE", "सेब"), ("MANGO", "आम"), ("BANANA", "केला"),
        ("ORANGE", "संतरा"), ("WATERMELON", "तरबूज़"), ("GRAPES", "अंगूर"),
        ("PINEAPPLE", "अनानास"), ("STRAWBERRY", "स्ट्रॉबेरी"), ("PAPAYA", "पपीता"),
        ("POMEGRANATE", "अनार")]),
    "VEGETABLES": ("सब्ज़ियाँ", [
        ("POTATO", "आलू"), ("TOMATO", "टमाटर"), ("CARROT", "गाजर"),
        ("ONION", "प्याज़"), ("SPINACH", "पालक"), ("CABBAGE", "पत्तागोभी"),
        ("CAULIFLOWER", "फूलगोभी"), ("PEAS", "मटर"), ("CORN", "मक्का"),
        ("CUCUMBER", "खीरा")]),
    "DRINKS": ("पेय", [
        ("WATER", "पानी"), ("TEA", "चाय"), ("COFFEE", "कॉफ़ी"),
        ("LEMONADE", "नींबू पानी"), ("MILK", "दूध"), ("JUICE", "जूस"),
        ("SMOOTHIE", "स्मूदी"), ("MILKSHAKE", "मिल्कशेक"), ("LASSI", "लस्सी"),
        ("COCONUT WATER", "नारियल पानी")]),
    "DESSERTS": ("मिठाइयाँ", [
        ("ICE CREAM", "आइसक्रीम"), ("CAKE", "केक"), ("DONUT", "डोनट"),
        ("BROWNIE", "ब्राउनी"), ("GULAB JAMUN", "गुलाब जामुन"), ("JALEBI", "जलेबी"),
        ("KHEER", "खीर"), ("PUDDING", "पुडिंग"), ("CUPCAKE", "कपकेक"),
        ("RASGULLA", "रसगुल्ला")]),
    "SPORTS": ("खेल", [
        ("CRICKET", "क्रिकेट"), ("FOOTBALL", "फुटबॉल"), ("BASKETBALL", "बास्केटबॉल"),
        ("TENNIS", "टेनिस"), ("BADMINTON", "बैडमिंटन"), ("VOLLEYBALL", "वॉलीबॉल"),
        ("HOCKEY", "हॉकी"), ("BOXING", "मुक्केबाज़ी"), ("SWIMMING", "तैराकी"),
        ("WRESTLING", "कुश्ती")]),
    "VEHICLES": ("वाहन", [
        ("CAR", "कार"), ("BUS", "बस"), ("TRAIN", "ट्रेन"), ("BICYCLE", "साइकिल"),
        ("MOTORCYCLE", "मोटरसाइकिल"), ("SCOOTER", "स्कूटर"), ("AIRPLANE", "हवाई जहाज़"),
        ("HELICOPTER", "हेलीकॉप्टर"), ("BOAT", "नाव"), ("TRUCK", "ट्रक")]),
    "PLACES": ("स्थान", [
        ("AIRPORT", "हवाई अड्डा"), ("HOSPITAL", "अस्पताल"), ("SCHOOL", "स्कूल"),
        ("BEACH", "समुद्र तट"), ("CASTLE", "किला"), ("MUSEUM", "संग्रहालय"),
        ("CINEMA", "सिनेमा"), ("RESTAURANT", "रेस्तरां"), ("LIBRARY", "पुस्तकालय"),
        ("PARK", "पार्क")]),
    "PROFESSIONS": ("पेशे", [
        ("DOCTOR", "डॉक्टर"), ("TEACHER", "शिक्षक"), ("ENGINEER", "इंजीनियर"),
        ("CHEF", "रसोइया"), ("PILOT", "पायलट"), ("POLICE OFFICER", "पुलिस अधिकारी"),
        ("FIREFIGHTER", "दमकलकर्मी"), ("FARMER", "किसान"), ("ARTIST", "कलाकार"),
        ("SCIENTIST", "वैज्ञानिक")]),
    "CLOTHES": ("कपड़े", [
        ("SHIRT", "कमीज़"), ("T-SHIRT", "टी-शर्ट"), ("JEANS", "जींस"),
        ("DRESS", "पोशाक"), ("SKIRT", "स्कर्ट"), ("JACKET", "जैकेट"),
        ("SWEATER", "स्वेटर"), ("SHORTS", "शॉर्ट्स"), ("SAREE", "साड़ी"),
        ("KURTA", "कुर्ता")]),
    "FURNITURE": ("फर्नीचर", [
        ("CHAIR", "कुर्सी"), ("TABLE", "मेज़"), ("SOFA", "सोफ़ा"), ("BED", "बिस्तर"),
        ("DESK", "डेस्क"), ("CUPBOARD", "अलमारी"), ("BOOKSHELF", "किताबों की अलमारी"),
        ("BENCH", "बेंच"), ("STOOL", "स्टूल"), ("WARDROBE", "कपड़ों की अलमारी")]),
    "KITCHEN": ("रसोई", [
        ("PLATE", "प्लेट"), ("SPOON", "चम्मच"), ("FORK", "कांटा"), ("KNIFE", "चाकू"),
        ("PAN", "कड़ाही"), ("KETTLE", "केतली"), ("BLENDER", "मिक्सर"),
        ("OVEN", "ओवन"), ("REFRIGERATOR", "फ़्रिज"), ("PRESSURE COOKER", "प्रेशर कुकर")]),
    "BATHROOM": ("बाथरूम", [
        ("TOOTHBRUSH", "टूथब्रश"), ("TOOTHPASTE", "टूथपेस्ट"), ("SOAP", "साबुन"),
        ("SHAMPOO", "शैम्पू"), ("TOWEL", "तौलिया"), ("MIRROR", "आईना"),
        ("BATHTUB", "बाथटब"), ("SHOWER", "शॉवर"), ("COMB", "कंघी"), ("BUCKET", "बाल्टी")]),
    "SCHOOL": ("स्कूल", [
        ("BOOK", "किताब"), ("NOTEBOOK", "कॉपी"), ("PENCIL", "पेंसिल"), ("ERASER", "रबर"),
        ("RULER", "स्केल"), ("BACKPACK", "स्कूल बैग"), ("CLASSROOM", "कक्षा"),
        ("BLACKBOARD", "श्यामपट्ट"), ("HOMEWORK", "गृहकार्य"), ("EXAM", "परीक्षा")]),
    "TECHNOLOGY": ("प्रौद्योगिकी", [
        ("SMARTPHONE", "स्मार्टफ़ोन"), ("COMPUTER", "कंप्यूटर"), ("LAPTOP", "लैपटॉप"),
        ("KEYBOARD", "कीबोर्ड"), ("MOUSE", "माउस"), ("ROBOT", "रोबोट"),
        ("CAMERA", "कैमरा"), ("TELEVISION", "टेलीविज़न"), ("HEADPHONES", "हेडफ़ोन"),
        ("DRONE", "ड्रोन")]),
    "HOME": ("घर", [
        ("DOOR", "दरवाज़ा"), ("WINDOW", "खिड़की"), ("LAMP", "लैंप"), ("FAN", "पंखा"),
        ("CLOCK", "घड़ी"), ("CURTAIN", "परदा"), ("PILLOW", "तकिया"), ("BLANKET", "कंबल"),
        ("CARPET", "कालीन"), ("CANDLE", "मोमबत्ती")]),
    "NATURE": ("प्रकृति", [
        ("MOUNTAIN", "पहाड़"), ("VOLCANO", "ज्वालामुखी"), ("FOREST", "जंगल"),
        ("WATERFALL", "झरना"), ("DESERT", "रेगिस्तान"), ("RIVER", "नदी"),
        ("LAKE", "झील"), ("RAINBOW", "इंद्रधनुष"), ("GLACIER", "हिमनद"),
        ("ISLAND", "द्वीप")]),
    "WEATHER": ("मौसम", [
        ("RAIN", "बारिश"), ("SNOW", "बर्फ़बारी"), ("THUNDER", "गरज"),
        ("LIGHTNING", "बिजली"), ("CLOUD", "बादल"), ("WIND", "हवा"),
        ("FOG", "कोहरा"), ("STORM", "तूफ़ान"), ("HAIL", "ओले"), ("SUNSHINE", "धूप")]),
    "SPACE": ("अंतरिक्ष", [
        ("SUN", "सूरज"), ("MOON", "चाँद"), ("EARTH", "पृथ्वी"), ("MARS", "मंगल"),
        ("JUPITER", "बृहस्पति"), ("STAR", "तारा"), ("PLANET", "ग्रह"), ("ROCKET", "रॉकेट"),
        ("ASTRONAUT", "अंतरिक्ष यात्री"), ("SATELLITE", "उपग्रह")]),
    "MUSIC": ("संगीत", [
        ("GUITAR", "गिटार"), ("PIANO", "पियानो"), ("DRUMS", "ड्रम"), ("VIOLIN", "वायलिन"),
        ("FLUTE", "बांसुरी"), ("TRUMPET", "तुरही"), ("MICROPHONE", "माइक्रोफ़ोन"),
        ("SINGER", "गायक"), ("CONCERT", "संगीत कार्यक्रम"), ("DJ", "डीजे")]),
    "MOVIES": ("फ़िल्में", [
        ("SUPERHERO", "सुपरहीरो"), ("VILLAIN", "खलनायक"), ("ACTOR", "अभिनेता"),
        ("DIRECTOR", "निर्देशक"), ("CINEMA", "सिनेमा"), ("TICKET", "टिकट"),
        ("MONSTER", "राक्षस"), ("PRINCESS", "राजकुमारी"), ("DETECTIVE", "जासूस"),
        ("COMEDY", "कॉमेडी")]),
    "GAMES": ("गेम्स", [
        ("CHESS", "शतरंज"), ("CARDS", "ताश"), ("DICE", "पासा"), ("VIDEO GAME", "वीडियो गेम"),
        ("PUZZLE", "पहेली"), ("HIDE AND SEEK", "लुका-छिपी"), ("TAG", "पकड़म-पकड़ाई"),
        ("LUDO", "लूडो"), ("CARROM", "कैरम"), ("RACING GAME", "रेसिंग गेम")]),
    "TOYS": ("खिलौने", [
        ("TEDDY BEAR", "टेडी बियर"), ("DOLL", "गुड़िया"), ("TOY CAR", "खिलौना कार"),
        ("BALL", "गेंद"), ("YO-YO", "यो-यो"), ("KITE", "पतंग"), ("PUZZLE CUBE", "पहेली घन"),
        ("TOY TRAIN", "खिलौना ट्रेन"), ("BUILDING BLOCKS", "खिलौना ब्लॉक"), ("TOY ROBOT", "खिलौना रोबोट")]),
    "TRAVEL": ("यात्रा", [
        ("PASSPORT", "पासपोर्ट"), ("SUITCASE", "सूटकेस"), ("MAP", "नक्शा"), ("TOURIST", "पर्यटक"),
        ("HOTEL", "होटल"), ("BEACH", "समुद्र तट"), ("AIRPORT", "हवाई अड्डा"),
        ("TRAIN STATION", "रेलवे स्टेशन"), ("CAMERA", "कैमरा"), ("COMPASS", "दिशासूचक")]),
    "BODY": ("शरीर", [
        ("HEAD", "सिर"), ("EYE", "आँख"), ("EAR", "कान"), ("NOSE", "नाक"),
        ("MOUTH", "मुँह"), ("HAND", "हाथ"), ("FINGER", "उंगली"), ("FOOT", "पैर"),
        ("HEART", "दिल"), ("BRAIN", "दिमाग")]),
    "EMOTIONS": ("भावनाएँ", [
        ("HAPPINESS", "खुशी"), ("SADNESS", "उदासी"), ("ANGER", "गुस्सा"), ("FEAR", "डर"),
        ("LOVE", "प्यार"), ("SURPRISE", "आश्चर्य"), ("EXCITEMENT", "उत्साह"),
        ("JEALOUSY", "ईर्ष्या"), ("CONFUSION", "उलझन"), ("PRIDE", "गर्व")]),
    "CELEBRATIONS": ("उत्सव", [
        ("BIRTHDAY", "जन्मदिन"), ("WEDDING", "शादी"), ("FESTIVAL", "त्योहार"),
        ("DIWALI", "दिवाली"), ("HOLI", "होली"), ("CHRISTMAS", "क्रिसमस"),
        ("EID", "ईद"), ("FIREWORKS", "आतिशबाज़ी"), ("GIFT", "उपहार"), ("PARTY", "पार्टी")]),
    "COUNTRIES": ("देश", [
        ("INDIA", "भारत"), ("JAPAN", "जापान"), ("FRANCE", "फ़्रांस"), ("BRAZIL", "ब्राज़ील"),
        ("CANADA", "कनाडा"), ("AUSTRALIA", "ऑस्ट्रेलिया"), ("EGYPT", "मिस्र"),
        ("ITALY", "इटली"), ("CHINA", "चीन"), ("NEPAL", "नेपाल")]),
    "CITY LIFE": ("शहरी जीवन", [
        ("TRAFFIC", "यातायात"), ("METRO", "मेट्रो"), ("TRAFFIC LIGHT", "ट्रैफ़िक लाइट"),
        ("MALL", "मॉल"), ("MARKET", "बाज़ार"), ("APARTMENT", "अपार्टमेंट"),
        ("TAXI", "टैक्सी"), ("BUS STOP", "बस स्टॉप"), ("STREET", "सड़क"),
        ("SKYSCRAPER", "गगनचुंबी इमारत")]),
    "FARM": ("खेत", [
        ("COW", "गाय"), ("HORSE", "घोड़ा"), ("CHICKEN", "मुर्गी"), ("GOAT", "बकरी"),
        ("SHEEP", "भेड़"), ("TRACTOR", "ट्रैक्टर"), ("BARN", "खलिहान"), ("FARMER", "किसान"),
        ("WHEAT", "गेहूँ"), ("RICE", "चावल")]),
    "SEA": ("समुद्र", [
        ("SHARK", "शार्क"), ("WHALE", "व्हेल"), ("OCTOPUS", "ऑक्टोपस"), ("CRAB", "केकड़ा"),
        ("TURTLE", "कछुआ"), ("SEASHELL", "समुद्री सीप"), ("CORAL", "प्रवाल"),
        ("SUBMARINE", "पनडुब्बी"), ("LIGHTHOUSE", "प्रकाशस्तंभ"), ("WAVE", "लहर")]),
    "COLORS": ("रंग", [
        ("RED", "लाल"), ("BLUE", "नीला"), ("GREEN", "हरा"), ("YELLOW", "पीला"),
        ("ORANGE", "नारंगी"), ("PURPLE", "बैंगनी"), ("PINK", "गुलाबी"), ("BLACK", "काला"),
        ("WHITE", "सफ़ेद"), ("BROWN", "भूरा")]),
}

# Keep the existing game interface: game_logic can still randomly choose an entry.
WORD_DATABASE = [
    {
        "word": word_en,
        "word_hi": word_hi,
        "category": category_en,
        "category_hi": category_hi,
    }
    for category_en, (category_hi, entries) in CATEGORY_DATA.items()
    for word_en, word_hi in entries
]

# 30 categories × 10 words = 300 curated bilingual entries.
