#include <inttypes.h>
#include <string>
#include <tsl/ordered_map.h>

typedef tsl::ordered_map<int64_t, int64_t, std::hash<int64_t>> hash_t;
typedef tsl::ordered_map<std::string, int64_t, std::hash<std::string>> str_hash_t;

#define SETUP hash_t hash; str_hash_t str_hash;

#define RESERVE_INT(size) hash.reserve(size);
#define RESERVE_STR(size) str_hash.reserve(size); 
#define LOAD_FACTOR(map) map.load_factor()

#define INSERT_INT_INTO_HASH(key, value) hash.insert(hash_t::value_type(key, value))
#define DELETE_INT_FROM_HASH(key) hash.unordered_erase(key)
#define FIND_INT_EXISTING_FROM_HASH(key) if(hash.find(key) == hash.end()) { printf("error"); exit(1); }
#define FIND_INT_MISSING_FROM_HASH(key) if(hash.find(key) != hash.end()) { printf("error"); exit(2); }
#define FIND_INT_EXISTING_FROM_HASH_COUNT(key, count) \
    if(hash.find(key) != hash.end()) { count++; }
#define CHECK_INT_ITERATOR_VALUE(iterator, value) if(iterator->second != value) { printf("error"); exit(3); }

#define INSERT_STR_INTO_HASH(key, value) str_hash.insert(str_hash_t::value_type(key, value))
#define DELETE_STR_FROM_HASH(key) str_hash.unordered_erase(key);
#define FIND_STR_EXISTING_FROM_HASH(key) if(str_hash.find(key) == str_hash.end()) { printf("error"); exit(4); }
#define FIND_STR_MISSING_FROM_HASH(key) if(str_hash.find(key) != str_hash.end()) { printf("error"); exit(5); }
#define FIND_STR_EXISTING_FROM_HASH_COUNT(key, count) \
    if(str_hash.find(key) != str_hash.end()) { count++; }

#include "template.c"

