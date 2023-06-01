use('mltask');

db.createCollection('quries')
db.createCollection('resources')

db.getCollection('resources').insertMany([
    {'type': 'article',
    'name': `The problem of information overload in business organisations:
a review of the literature`,
    'author': 'Angela Edmunds, Anne Morris',
    'year': 2000,
    'publisher': 'International Journal of Information Management',
    'summary': `This paper reviews the literature on the problem of information overload, with particular reference to business organisations. A theme stressed in the literature is the paradoxical situation that it is often difficult to obtain useful, relevant infor-\nmation when it is needed. An emphasis is placed on technology as a tool and not the driver.`,
    'sentiment': 'positive'
    
    }
])

