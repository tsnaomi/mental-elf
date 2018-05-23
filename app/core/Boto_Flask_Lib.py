import boto3
# from flask import Flask

# Open DynamoDB
def Open_DynamoDB(Table_Name):
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Load a specific table
    table = dynamodb.Table(Table_Name)

    return table

# Write single item
def Cerate_Item(table, item):
    table.put_item(Item = item)

# Write multiple item
def Write_Batch(table, batch_list):
    with table.batch_writer() as batch:
        for i in range(len(batch_list)):
            batch.put_item(Item = batch_list[i])

# Get specific items
def Get_Item(table, key):
    response = table.get_item(Key = key)
    item = response['Item']

    return item

# Update items
'''
Example input:
express = 'SET age = :val1'
value = {':val1': 26}
'''
def Update_Item(table, key, express, value):
    table.update_item(Key = key, UpdateExpression = express, ExpressionAttributeValues = value)

# Delete items
def Delete_Item(table, key):
    table.delete_item(Key = key)


'''
# Main function
if __name__ == '__main__':
    Table_Name = 'users'
    
    app = Flask(__name__)
    table = Open_DynamoDB(Table_Name)
    
    @app.route('/')
    def hello():
        Key = {
            'username': 'janedoe',
            'last_name': 'Doe'
        }
        item = Get_Item(table, Key)
        return str(item['age'])
    
    app.run()
'''

