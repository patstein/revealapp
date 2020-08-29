# To build and run:
## Everything

    sudo docker-compose -f build/docker-compose.yml up -d --build

# To stop 
## Everything
    sudo docker-compose -f build/docker-compose.yml stop
    

# To invoke APIs:
## GET

    #local
    curl localhost:8889/healthz

    #from remote:
    curl 128.199.179.79:8889/healthz

## POST

### To Post documents
Once the documents have been uploaded to the platform the documents can be posted through the API to the DataScience webserver. For this the entire documents table (with columns ID and FullText) needs to be sent in json format.

Syntax:

    curl http://128.199.179.79:8889/postDocuments -d '<YOUR_DOCUMENT_TABLE_AS_JSON>' -H 'Content-Type: application/json'

Example: 

    curl http://128.199.179.79:8889/postDocuments -d '[{"id_pdf":1,"id_user":1,"id_tag":1,"PDFfile":"doc1.pdf","title":"doc1","content_text":"This is a random document with ID 1. In this document we are talking about cats. And there is also something about mice.","content_html":"<p>This is a random document with ID 1.\\r\\nIn this document we are talking about cats. And there is also something about mice.","date_uploaded":"2020-04-17T18:31:49.372861+02:00"},{"id_pdf":2,"id_user":1,"id_tag":1,"PDFfile":"doc2.pdf","title":"doc2","content_text":"This is a random document with ID 2. In this document we are talking about dogs. And there is also something about mice.","content_html":"<p>This is a random document with ID 2. In this document we are talking about dogs.\\r\\nAnd there is also something about mice.","date_uploaded":"2020-04-17T18:31:49.372861+02:00"},{"id_pdf":2,"id_user":1,"id_tag":1,"PDFfile":"bla3.pdf","title":"bla3","content_text":"This is a random document with ID 3. this doc is exclusivly about Elephants. So no mice, cats nor anything else","content_html":"<p>This is a random document with ID 3. this doc is exclusivly about Elephants.\r\nSo no mice, cats nor anything else","date_uploaded":"2020-04-17T18:31:49.372861+02:00"}]' -H 'Content-Type: application/json'



### To generate new suggested tags from tags
If the "Suggest"-Button is hit by the user the tags table is sent to the DataScience webserver through the API in json format.

Syntax:

    curl http://128.199.179.79:8889/suggestTags -d '<YOUR_TAGS_TABLE_AS_JSON>' -H 'Content-Type: application/json' 

Example:

    curl http://128.199.179.79:8889/suggestTags -d '[{"id_highlight":1,"id_pdf":1,"id_user":1,"id_tag":1,"starting_point":37,"ending_point":80,"selection":" In this document we are talking about cats.","suggested":0,"score":null,"id_parent_highlight":null,"accepted":null,"date_created":"2020-04-17T18:31:49.372861+02:00","date_updated":"2020-04-17T18:31:49.372861+02:00"},{"id_highlight":2,"id_pdf":1,"id_user":1,"id_tag":2,"starting_point":80,"ending_point":120,"selection":" And there is also something about mice.","suggested":0,"score":null,"id_parent_highlight":null,"accepted":null,"date_created":"2020-04-17T18:32:49.372861+02:00","date_updated":"2020-04-17T18:32:49.372861+02:00"}]' -H 'Content-Type: application/json'



### To generated new suggested tags based on userfeedback in suggested tags table 
If the "Train&Suggest"-Button is hit by the user, the tags table together with the suggested tags table is sent to the DataScience webserver through the API in json format.


Syntax:

    curl http://128.199.179.79:8889/trainSuggest -d '<"tags":<YOUR_TAGS_TABLE_JSON>' -H 'Content-Type: application/json'

Example:

    curl http://128.199.179.79:8889/trainSuggest -d '[{"id_highlight":1,"id_pdf":1,"id_user":1,"id_tag":1,"starting_point":37,"ending_point":80,"selection":" In this document we are talking about cats.","suggested":0,"score":null,"id_parent_highlight":null,"accepted":null,"date_created":"2020-04-17T18:31:49.372861+02:00","date_updated":"2020-04-17T18:31:49.372861+02:00"},{"id_highlight":2,"id_pdf":1,"id_user":1,"id_tag":2,"starting_point":80,"ending_point":120,"selection":" And there is also something about mice.","suggested":0,"score":null,"id_parent_highlight":null,"accepted":null,"date_created":"2020-04-17T18:32:49.372861+02:00","date_updated":"2020-04-17T18:32:49.372861+02:00"},{"id_highlight":3,"id_pdf":1,"id_user":1,"id_tag":1,"starting_point":80,"ending_point":120,"selection":" And there is also something about mice.","suggested":1,"score":0.74,"id_parent_highlight":1.0,"accepted":null,"date_created":"2020-04-17T18:35:49.372861+02:00","date_updated":"2020-04-17T18:35:49.372861+02:00"},{"id_highlight":4,"id_pdf":2,"id_user":1,"id_tag":1,"starting_point":80,"ending_point":120,"selection":" And there is also something about mice.","suggested":1,"score":0.74,"id_parent_highlight":1.0,"accepted":null,"date_created":"2020-04-17T18:35:49.372861+02:00","date_updated":"2020-04-17T18:35:49.372861+02:00"},{"id_highlight":5,"id_pdf":3,"id_user":1,"id_tag":1,"starting_point":36,"ending_point":76,"selection":"this doc is exclusivly about Elephants.","suggested":1,"score":0.5,"id_parent_highlight":1.0,"accepted":null,"date_created":"2020-04-17T18:35:49.372861+02:00","date_updated":"2020-04-17T18:35:49.372861+02:00"},{"id_highlight":6,"id_pdf":3,"id_user":1,"id_tag":1,"starting_point":76,"ending_point":112,"selection":" So no mice, cats nor anything else.","suggested":1,"score":0.44,"id_parent_highlight":2.0,"accepted":null,"date_created":"2020-04-17T18:35:49.372861+02:00","date_updated":"2020-04-17T18:35:49.372861+02:00"}]' -H 'Content-Type: application/json'

