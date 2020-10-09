import boto3
import datetime



def checkForTable(tableName):
    table_exist=False
    dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
    tables = dynamodb.list_tables()
    if tableName in tables["TableNames"]:
        table_exist=True
    return table_exist


def CreateStoreTable():
    table_exist=checkForTable("MyStore")
    if not table_exist:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb.create_table(
            TableName='MyStore',
            KeySchema=[
                {
                    'AttributeName': 'ItemName',
                    'KeyType': 'HASH'  # Partition key
                }
                ],
                AttributeDefinitions=[
                {
                    'AttributeName': 'ItemName',


                    'AttributeType': 'S'
                },

                ],
                ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
                )
        PopulateStore()
        return 'MyStore Table Created '
    else:
        return 'MyStore Table Exist '

def CreateShoppingCart(name):
    table_exist=checkForTable(name)
    if not table_exist:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb.create_table(
            TableName=name,
            KeySchema=[
                {
                    'AttributeName': 'ItemName',
                    'KeyType': 'HASH'  # Partition key
                }
                ],
                AttributeDefinitions=[
                {
                    'AttributeName': 'ItemName',
                    'AttributeType': 'S'
                },

                ],
                ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
                )
        return 'Shopping Cart Created '
    else:
        return 'Shopping Cart Exist '

def CreateReceiptTable(name):
    table_exist=checkForTable(name)
    if not table_exist:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb.create_table(
            TableName=name,
            KeySchema=[
                {
                    'AttributeName': 'ReceiptId',
                    'KeyType': 'HASH'  # Partition key
                }
                ],
                AttributeDefinitions=[
                {
                    'AttributeName': 'ReceiptId',
                    'AttributeType': 'N'
                },

                ],
                ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
                )
        if name == 'wrislin_Receipts':
            PopulateReceipt()
        return 'Receipt Table Created '
    else:
        return 'Receipt Table Exist '

def CreateTableUsers():
    table_exist=checkForTable("Users")
    if not table_exist:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb.create_table(
            TableName='Users',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'  # Partition key
                }
                ],
                AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },

                ],
                ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
                )
        PopulateUsers()
        return 'Users Table Created '
    else:
        return 'Users Table Exist '


def PopulateUsers():
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table=dynamodb.Table("Users")
    user={'username':'wrislin','password':'password'}
    table.put_item(Item=user)

def PopulateStore():
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table=dynamodb.Table("MyStore")
    StoreItems=[
            {"ItemName": "Item1","price": 100,"stock": 3},
            {"ItemName": "Item2","price": 200,"stock": 3},
            {"ItemName": "Item3","price": 75,"stock": 3},
            {"ItemName": "Item4","price": 30,"stock": 3},
            {"ItemName": "Item5","price": 18,"stock": 3},
            {"ItemName": "Item6","price": 17,"stock": 3},
            {"ItemName": "Item7","price": 22,"stock": 3},
            {"ItemName": "Item8","price": 53,"stock": 3},
            {"ItemName": "Item9","price": 44,"stock": 3},
            {"ItemName": "Item10","price": 355,"stock": 3},
            {"ItemName": "Item11","price": 27,"stock": 3}
            ]

    for entry in StoreItems:
        table.put_item(Item=entry)

def PopulateReceipt():
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    ReceiptEntries=[{"ReceiptId":13, "SubTotal": 100,"Items":[{"ItemName":"Item1","price": 100, 'TotalCost':100,"Amount":1}],"date":"2019-02-15"},
        {"ReceiptId":1, "SubTotal": 100,"Items":[{"ItemName":"Item1","price": 100,"Amount":1, 'TotalCost': 100}],"date":"2019-03-15"},
        {"ReceiptId":2, "SubTotal": 200,"Items":[{"ItemName":"Item2","price": 200,"Amount":1, 'TotalCost':200}], "date":"2020-01-11"},
        {"ReceiptId":3, "SubTotal": 75,"Items":[{"ItemName":"Item3","price": 75,"Amount":1, 'TotalCost':75}], "date":"2018-02-08"},
        {"ReceiptId":4, "SubTotal": 30,"Items":[{"ItemName":"Item4","price": 30,"Amount":1, 'TotalCost':30}],"date":"2020-12-14"},
        {"ReceiptId":5, "SubTotal": 18,"Items":[{"ItemName":"Item5","price": 18,"Amount":1, 'TotalCost':18}], "date":"2018-05-07"},
        {"ReceiptId":6, "SubTotal": 200,"Items":[{"ItemName":"Item12","price": 200,"Amount":1, 'TotalCost':200}], "date":"2018-04-30"},
        {"ReceiptId":7, "SubTotal": 75,"Items":[{"ItemName":"Item13","price": 75,"Amount":1, 'TotalCost':75}], "date":"2019-08-06"},
        {"ReceiptId":8, "SubTotal": 30,"Items":[{"ItemName":"Item14","price": 30,"Amount":1, 'TotalCost':30}], "date":"2020-09-04"},
        {"ReceiptId":9, "SubTotal": 22,"Items":[{"ItemName":"Item17","price": 22,"Amount":1, 'TotalCost':22}], "date":"2018-05-25"},
        {"ReceiptId":10, "SubTotal": 17,"Items":[{"ItemName":"Item16","price": 17,"Amount":1, 'TotalCost':17}],"date":"2020-10-02"},
        {"ReceiptId":11, "SubTotal": 53,"Items":[{"ItemName":"Item18","price": 53,"Amount":1, 'TotalCost':53}], "date":"2019-01-13"},
        {"ReceiptId":12, "SubTotal": 30,"Items":[{"ItemName":"Item14","price": 30,"Amount":1, 'TotalCost':30}], "date":"2020-08-23"}]
    table=dynamodb.Table("wrislin_Receipts")
    for receipt in ReceiptEntries:
        table.put_item(Item=receipt)
