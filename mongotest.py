import pymongo



class MogoTest():

    def __init__(self):
        print('MogoTest>>>>')

    def insert_one_test(self, collection):
        print('insert_one_test>>>>')
        student = {
            'id': '20170101',
            'name': 'Jordan',
            'age': 20,
            'gender': 'male'
        }

        # result = collection.insert(student)
        result = collection.insert_one(student)
        print(result)
        print(result.inserted_id)
        print('---------------------------------')

        student1 = {
            'id': '20170101',
            'name': 'Jordan',
            'age': 20,
            'gender': 'male'
        }

        student2 = {
            'id': '20170202',
            'name': 'Mike',
            'age': 21,
            'gender': 'male'
        }

        result = collection.insert_many([student1, student2])
        print(result)
        print(result.inserted_ids)

if __name__ == '__main__':
    print('__mian__>>>>')
    client = pymongo.MongoClient(host='localhost', port=27017)
    # client = MongoClient('mongodb://localhost:27017/')

    db = client['test']
    collection = db['students']
    print(db)
    print(collection)
    print('---------------------------------')

    # test = MogoTest()
    # test.insert_one_test(collection)

    ff = collection.find()
    print(list(ff))
    count = collection.find().count()
    print(count)

    client.close()
