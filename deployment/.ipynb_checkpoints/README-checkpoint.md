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
    curl 134.209.231.8:8889/healthz

## POST

### To Post documents
'''
    curl http://134.209.231.8:8889/postDocuments -d '{"ID":{"0":1, "1": 2}, "FullText": {"0":"Doc1", "1":"Doc2"}}' -H 'Content-Type: application/json'
'''

### To generate new suggested tags from tags
'''
curl http://134.209.231.8:8889/suggestTags -d '{"ID":{"0":1,"1":2},"DocID":{"0":1,"1":1},"startIdx":{"0":37,"1":81},"Length":{"0":43,"1":39}}' -H 'Content-Type: application/json' 
'''

### To generated new suggested tags based on userfeedback in suggested tags table 
'''
    curl http://134.209.231.8:8889/trainSuggest -d '{"tags":{"ID":{"0":1,"1":2},"DocID":{"0":1,"1":1},"startIdx":{"0":37,"1":81},"Length":{"0":43,"1":39}}, "suggTags":{"ID":{"0":1,"1":2,"2":3,"3":4},"DocID":{"0":1,"1":2,"2":3,"3":3},"startIdx":{"0":81,"1":81,"2":37,"3":77},"Length":{"0":39,"1":39,"2":39,"3":34},"TagID":{"0":1,"1":1,"2":1,"3":1},"SimilarityScore":{"0":0.74,"1":0.5,"2":0.8,"3":0.77},"Accepted":{"0":null,"1":0.0,"2":1.0,"3":1.0}} }' -H 'Content-Type: application/json'
'''    