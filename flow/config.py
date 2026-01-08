index_settings = {
    "settings": {
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_" 
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "light_english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                }
            },
            "analyzer": {
                "my_english_analyzer": {
                    "tokenizer": "standard",
                    "filter": ["lowercase",
                               "english_stop",
                               "english_stemmer",
                               "english_possessive_stemmer"
                              ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "my_english_analyzer",
                "search_analyzer": "my_english_analyzer"
            },
            "subtitles": {
                "type": "text",
                "analyzer": "my_english_analyzer",
                "search_analyzer": "my_english_analyzer"
            }
        }
    }
}
