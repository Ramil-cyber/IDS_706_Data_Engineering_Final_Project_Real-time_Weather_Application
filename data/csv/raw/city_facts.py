import pandas as pd

city_facts = [
    (0, "New York", "New York", "Known as the 'City That Never Sleeps' due to its vibrant nightlife. New York is also home to the Statue of Liberty, a symbol of freedom and democracy."),
    (1, "Los Angeles", "California", "Home to Hollywood, the entertainment capital of the world. Los Angeles has more than 75 miles of coastline, making it a prime location for beach lovers."),
    (2, "Chicago", "Illinois", "Chicago is home to the world’s first skyscraper, built in 1885. Chicago is also known for its deep-dish pizza, a must-try for foodies."),
    (3, "Houston", "Texas", "Houston is the largest city in Texas and a hub for the energy industry. Houston is home to NASA’s Johnson Space Center, where space missions are controlled."),
    (4, "Philadelphia", "Pennsylvania", "Philadelphia is home to the Liberty Bell, a symbol of American independence. Philadelphia is also known for its famous Philly cheesesteaks."),
    (5, "Phoenix", "Arizona", "Phoenix is one of the sunniest cities in the U.S., with over 300 sunny days each year. Phoenix is also known for its desert botanical gardens, showcasing unique desert flora."),
    (6, "San Antonio", "Texas", "San Antonio is famous for the Alamo, a historic site of the Texas Revolution. San Antonio is home to the River Walk, a scenic area filled with shops and restaurants."),
    (7, "San Diego", "California", "San Diego is home to the world-famous San Diego Zoo. San Diego is also known for its year-round mild climate, perfect for outdoor activities."),
    (8, "Dallas", "Texas", "Dallas is known for its modern architecture, including the famous Dallas Cowboys stadium. Dallas is also a major center for the arts, with a vibrant museum district."),
    (9, "San Jose", "California", "San Jose is the heart of Silicon Valley, home to many major tech companies. San Jose is known for its tech industry and is home to the Computer History Museum."),
    (10, "Austin", "Texas", "Austin is the ‘Live Music Capital of the World’ due to its vibrant music scene. Austin is also known for its food, particularly its BBQ and taco trucks."),
    (11, "Jacksonville", "Florida", "Jacksonville is the largest city by area in the U.S. Jacksonville boasts 22 miles of beaches, making it a paradise for beach lovers."),
    (12, "San Francisco", "California", "San Francisco is famous for the Golden Gate Bridge. San Francisco is also known for its diverse neighborhoods and famous cable cars."),
    (13, "Indianapolis", "Indiana", "Indianapolis hosts the famous Indianapolis 500 car race every year. Indianapolis is also home to the largest children's museum in the world."),
    (14, "Columbus", "Ohio", "Columbus is home to the Ohio State University, one of the largest universities in the U.S. Columbus is also known for its diverse culinary scene and historic architecture."),
    (15, "Fort Worth", "Texas", "Fort Worth is known for its historic Stockyards, showcasing cowboy culture. Fort Worth also has a thriving arts district, including the renowned Kimbell Art Museum."),
    (16, "Charlotte", "North Carolina", "Charlotte is known as the second-largest banking hub in the U.S. Charlotte is also famous for its NASCAR Hall of Fame and speedway."),
    (17, "Seattle", "Washington", "Seattle is home to the iconic Space Needle. Seattle is also known for its coffee culture, with Starbucks originating there."),
    (18, "Denver", "Colorado", "Denver is known as the Mile-High City, located exactly 5,280 feet above sea level. Denver is also famous for its craft beer scene, with many breweries across the city."),
    (19, "El Paso", "Texas", "El Paso is the largest U.S. city on the border with Mexico. El Paso is known for its blend of American and Mexican culture, including unique food and festivals."),
    (20, "Detroit", "Michigan", "Detroit is the birthplace of the American automobile industry. Detroit is also known for its rich music history, including the Motown sound."),
    (21, "Washington", "District of Columbia", "Washington, D.C. is the U.S. capital and home to national landmarks like the White House. Washington, D.C. is also famous for its museums, including the Smithsonian Institution."),
    (22, "Boston", "Massachusetts", "Boston is home to the first public park in the U.S., Boston Common. Boston is also known for its rich history, especially during the American Revolution."),
    (23, "Memphis", "Tennessee", "Memphis is the birthplace of blues music and home to Graceland, Elvis Presley’s mansion. Memphis is also famous for its barbecued ribs, a staple of Southern cuisine."),
    (24, "Nashville", "Tennessee", "Nashville is known as the ‘Music City’ due to its country music scene. Nashville is also known for its hot chicken, a spicy local dish."),
    (25, "Portland", "Oregon", "Portland is known for its eco-friendly culture and numerous parks. Portland is also famous for its food trucks, offering a wide variety of cuisines."),
    (26, "Oklahoma City", "Oklahoma", "Oklahoma City is home to the National Cowboy & Western Heritage Museum. Oklahoma City is also known for its thriving arts scene and outdoor activities."),
    (27, "Las Vegas", "Nevada", "Las Vegas is known for its vibrant nightlife centered around 24-hour casinos. Las Vegas is also home to the largest hotel in the world, The Venetian Resort."),
    (28, "Baltimore", "Maryland", "Baltimore is home to the U.S.S. Constellation, the oldest active-duty warship. Baltimore is also known for its crab cakes, a Maryland specialty."),
    (29, "Louisville", "Kentucky", "Louisville is famous for being the birthplace of the Kentucky Derby horse race. Louisville is also known for its bourbon, produced in the heart of the Bourbon Trail."),
    (30, "Milwaukee", "Wisconsin", "Milwaukee is known for its beer culture and is home to Miller Brewing Company. Milwaukee is also famous for its Harley-Davidson Museum, celebrating the iconic motorcycle brand."),
    (31, "Kansas City", "Missouri", "Kansas City is known for its jazz music and rich cultural history. Kansas City is also famous for its barbecue, particularly its unique style of sauce."),
    (32, "Cleveland", "Ohio", "Cleveland is home to the Rock and Roll Hall of Fame. Cleveland is also known for its thriving theater scene, particularly the Cleveland Play House."),
    (33, "Tampa", "Florida", "Tampa is home to the historic Ybor City, known for its cigar-making culture. Tampa is also famous for its theme parks, including Busch Gardens."),
    (34, "Raleigh", "North Carolina", "Raleigh is known as the 'City of Oaks' for its many oak trees. Raleigh is also home to the North Carolina Museum of Natural Sciences."),
    (35, "Minneapolis", "Minnesota", "Minneapolis is known for its parks and over 13 lakes within the city limits. Minneapolis is also famous for its art scene, including the Walker Art Center."),
    (36, "St. Louis", "Missouri", "St. Louis is home to the Gateway Arch, the tallest man-made monument in the U.S. St. Louis is also known for its rich history in jazz and blues music."),
    (37, "Miami", "Florida", "Miami is famous for its vibrant nightlife and South Beach. Miami is also known for its cultural diversity, with a large Latin American influence."),
    (38, "Salt Lake City", "Utah", "Salt Lake City is home to the headquarters of The Church of Jesus Christ of Latter-day Saints. Salt Lake City is also known for its outdoor recreational opportunities, including skiing."),
    (39, "Tucson", "Arizona", "Tucson is known for its desert landscapes and unique cacti. Tucson is also home to the University of Arizona, a major research institution."),
    (40, "Anchorage", "Alaska", "Anchorage is the largest city in Alaska and a hub for Arctic exploration. Anchorage is also known for its outdoor activities, including hiking and dog sledding."),
    (41, "Fresno", "California", "Fresno is located in the heart of California's Central Valley and is a major agricultural hub. Fresno is also known for its proximity to national parks like Yosemite."),
    (42, "Birmingham", "Alabama", "Birmingham played a key role in the Civil Rights Movement. Birmingham is also known for its growing craft beer scene."),
    (43, "New Orleans", "Louisiana", "New Orleans is famous for its Mardi Gras celebrations. New Orleans is also known for its Creole cuisine, including gumbo and beignets."),
    (44, "St. Petersburg", "Florida", "St. Petersburg is known for having the most sunny days of any city in the U.S. St. Petersburg is also famous for its Salvador Dalí Museum."),
    (45, "Macon", "Georgia", "Macon is known as the 'Cherry Blossom Capital of the World.' Macon is also famous for being the birthplace of the Allman Brothers Band."),
    (46, "Lubbock", "Texas", "Lubbock is known as the birthplace of rock 'n' roll legend Buddy Holly. Lubbock is also home to Texas Tech University, a major research institution."),
    (47, "Shreveport", "Louisiana", "Shreveport is known for its casinos and riverboat culture. Shreveport is also famous for its Southern hospitality and vibrant local music scene."),
    (48, "Peoria", "Illinois", "Peoria is known for its long history in agriculture and as the birthplace of the Caterpillar Tractor Company. Peoria is also famous for its role in the development of the rail industry."),
    (49, "Grand Rapids", "Michigan", "Grand Rapids is known as 'Furniture City' for its history in the furniture industry. Grand Rapids is also famous for its craft breweries and arts scene.")
]

df = pd.DataFrame(city_facts, columns=['ID', 'city', 'state_name', 'fun_fact'])
df['fun_fact'] = df['fun_fact'].str.replace(r"(\. )", r" ", regex=True)

print(df[['city', 'state_name', 'fun_fact']].head())

df.to_csv('city_facts.csv', index=False)
print("CSV file 'city_facts.csv' created successfully.")