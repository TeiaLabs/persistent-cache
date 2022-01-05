# Available Cache Types


## Memory
A dictionary-based cache that stores values in-memory.
Stored variables are deleted after execution ends.


## Pickle
A [pickle](https://docs.python.org/3/library/pickle.html)-based cache.
Stored variables persist on disk via binary files in the pickle format.

**WARNING:** currently, every time we want to store a new key-value
pair in the cache, we rewrite the entire pickle binary file.


## DynamoDB
An [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)-based cache.
Stored variables persist on disk via a NoSQL database.

**WARNING:** DynamoDB limits the size of stored variables to 400KB.
Read more about it [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html).
