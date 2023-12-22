from pymongo import MongoClient
from pymongo.server_api import ServerApi
def conn():
    """
    Connects to the MongoDB Atlas cluster using the provided URI and credentials.

    Returns:
        A pymongo.database.Database object that represents the connected database.
    """
    uri = "mongodb+srv://hospital.amsaxop.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile='X509-cert-7723604173168106537.pem',
                        server_api=ServerApi('1'))

    db = client['Hospital']
    return db



# python -m pip install "pymongo[srv]"