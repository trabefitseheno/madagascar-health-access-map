# Demo script (target 2:30, limit 3:00)

**0:00 The problem (20 s)**
"In Madagascar, how long it takes to reach a health centre can decide whether a sick child gets care. Many families live hours from the nearest one."

**0:20 The data (30 s)**
"I used the Data for Children Collaborative travel-time dataset on HDX, licensed CC BY, published by Watmough and colleagues in Scientific Data. It gives motorised travel time to the nearest health centre at roughly 100 metre resolution. I turned it into four bands: under one hour, one to two, two to four, and over four hours."

**0:50 The map (40 s)**
[Open the live URL.] "Green is under an hour, yellow one to two, orange two to four, red over four. Notice the green clusters around the capital and the large red areas in the west and south." [Zoom, then click a shape.] "Clicking shows the band and the data credit."

**1:30 What you can explore (30 s)**
[Tick the facilities on.] "These dots are health facilities from OpenStreetMap. Notice how dense the east coast is and how empty the west looks, partly because of uneven mapping. Toggle bands to isolate the over-four-hour areas."
"Pan and zoom to your region. Compare coast and highlands. It works on a phone too." [Show mobile view.]

**2:00 AWS services (30 s)**
"The data and site live in a private S3 bucket. CloudFront with Origin Access Control serves them over HTTPS. Amazon Location Service provides the base map."

**2:30 Caveats and close (20 s)**
"Two caveats: the road data hasn't been validated, and health sites were filtered to those likely to offer child-focused services. Thank you."
