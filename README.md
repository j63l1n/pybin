# pybin

### What is it
Pybin is a plain text paste bin for code snippets or working modules. Initially supporting
python but could be extended to other languages. To be used with proper code formatting on
any device (mobile or desktop) using standard linter interactively.
Application should be able to share data through simple user_id/url.
Will maintain 20 last snippets with simple URI to be used from multiple devices.

### Requirements
* Upload
  * LIFO (stack) for simple last snippet using user_id
* TTL scrubber for time or max number of snippets
* _(Compression)_

### Design considerations
Key-value store to be used to maintain snippet with data. Logs to create permanent storage in 
buckets that can be accessed through separate API (history), TTL for those will be one year.
<br><br>
The latest snippet will always be available with the simple URI+user_id on any device.
<br>
Microservices should use gRPC when possible.<br>
Prefer self balanced trees for k/v store.<br>

### Capacity planning
#### Capacity (+ memory req)
* 1 Million users
* Traffic Estimates
    1. 100k Snippets per day (100k / day ~= 1 snippets/sec )
    2. 8:1 read versus write (800k reads / day ~= 9 reads/sec )
  
* Fully built out k/v:
   * around 1100 servers for key value
   * Given 80/20 rule it is likely that given TTL will cause a 20% full capacity e.g. 220 servers

* Fully built out DB
   * it is reasonable to believe that DB's will be 4 x size requirements of 240M * 1M *4 / 200 servers
  gives 5TB database per server with copies.

#### Size limits
* Max 10M of snippet, 2M of description Max per user (10M+2M) * 20 = 240M
* 1M users gives storage requirements to 240TB

#### Speed limits
* Rate limit based on user_id (60/min write, 800 /min read)
   * Using sliding window with counters, normalized to minutes
      * requires 2 x 4 bytes for epoch time and 2 bytes for counter

### API's
`addSnippet(api_dev_key,snip_desc,snip_data,user_id=None,snip_id=None,snip_ttl=12`

|type|name|default value|description|
|-----|-----|-----|-----|
|key|api_dev_key| |developer key to give response flexibility|
|text/snip_desc| |description of snippet|
|text|snip_data| |snippet to store|
|id|user_id|None|User unique ID|
|snippet id|snip_id|None|Snippet ID for the snippet|
|TTL|snip_ttl|12|Time to live for snippet in hours|

### K/V store

1. key user_id
2. dataobj (protobuf)

Needs to be redundant. Eventually consistent ok.<br>
Objects should support TTL.

### Database Design
Snip_id should be a hash to simplify partitioning.<br>
_Using url-shortening we can store detected github url that contains duplicate._<br>
![pybin_db](./images/pybindb_2.png)


### High level design
Service will require registration (google, facebook)<br>
Application will read and write requests. Logs get's sent to Cloud Store (ex. S3) and after
successful push trig an upload to history DB.<br>

    1. key for k/v store = user_id
    2. Contains counter for max items or 240MB size

![pybin highlevel](./images/pybinhigh3.png)
### Component design
### App layer
Application server relies on k/v store to initiate or retrieve user baselevel information,
e.g. max(counter)/used id's/ so it can retrieve existing buffer and push on to the stack.<br>
Linter will be used and will not commit until user corrects errors. After success adding blob
to k/v store and sending off to log pipeline. Keys will be simple using user_id with incremented snip number.


### Partitioning
### Load balancer
### Metrics
Evaluate sumo-logic for postgres monitors etc.<br>
Prometheus<br>
### Cache

### Future
* Duplication detection of snippet MD5
* Find snippets in GitHub

[just util and fun stuff](./fun_util)