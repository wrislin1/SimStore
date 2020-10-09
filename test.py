import boto3
from flask import Flask, render_template, request, redirect, url_for, flash,session
import PopulateTables
import datetime
import dateutil.parser
from decimal import Decimal
app = Flask(__name__)
app.secret_key = b'87tz#\x00"\xcc\x8a-\xa03L\x960\x13'

message=PopulateTables.CreateTableUsers()
message+=PopulateTables.CreateStoreTable()
print(message)
ShoppingCart=""
Receipts=""

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/login',methods=['GET','POST'])
def login():
    global ShoppingCart
    global Receipts
    if request.method=='GET':
        return render_template('login.html')
    else:
        users=List('Users')
        print (users)
        for user in users:
            print(user)
            if user['username'] == request.form['username'] and user['password'] == request.form['password']:
                session['username'] = request.form['username']
                ShoppingCart = session['username']+'_ShoppingCart'
                Receipts=session['username']+'_Receipts'
                PopulateTables.CreateShoppingCart(ShoppingCart)
                PopulateTables.CreateReceiptTable(Receipts)
                return redirect(url_for('ViewStore'))
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('ViewStore'))
    else:
        return redirect(url_for('login'))


@app.route('/store')
def ViewStore():
    return render_template('store.html',stores=List('MyStore'))

@app.route('/summary',methods=['POST','GET'])
def Summary():
    data=List(Receipts)
    if request.method=='GET':
        for d in data:
            date=dateutil.parser.parse(d["date"])
            d["date"]=date
        data.sort(reverse=True,key=dateSort)
    else:
        results=[]
        for r in data:
            for i in r['Items']:
                if request.form['SearchBar'] == i['ItemName']:
                    results.append(r)
                    break
        results.sort(reverse=True,key=dateSort)
        return render_template('summary.html',receipts=results)
    return render_template('summary.html',receipts=data)

@app.route('/receipt/<id>')
def ReceiptInfo(id=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    entry=dynamodb.Table(Receipts).get_item(Key={'ReceiptId':int(id)})
    entry=entry['Item']
    print(entry)
    print('-------------------------------------------------------------------------------------------------------------------------\n')
    print(entry)
    return render_template('receipt.html', data=entry)

@app.route('/newuser',methods=['POST','GET'])
def NewUser():
    if request.method=='GET':
        return render_template('newuser.html')
    else:
        table=List('Users')
        for user in table:
            if user['username']==request.form['username']:
                return redirect(url_for('NewUser'))
        entry={'username':request.form['username'],'password':request.form['password']}
        dynamodb=boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        table=dynamodb.Table('Users')
        table.put_item(Item=entry)
        print(List('Users'))
        return redirect(url_for('login'))


@app.route('/item/<name>',methods=['POST','GET'])
def itemInfo(name=None):
    if request.method=='GET':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        temp=dynamodb.Table("MyStore").get_item(Key={'ItemName':name})
        entry=temp['Item']
        return render_template('item.html', data=entry)
    else:
        ManagePost(name,request)
        return redirect(url_for('itemInfo',name=name))

@app.route('/checkout',methods=['POST', 'GET'])
def CheckOut():
    if request.method=='POST':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        table= dynamodb.Table(Receipts)
        date=datetime.datetime.now()
        entry ={'ReceiptId': len(List(Receipts))+1,'SubTotal':0,'Items': List(ShoppingCart),'date':datetime.datetime.now().strftime("%Y-%m-%d")}
        for e in entry['Items']:
            entry['SubTotal']+=e['TotalCost']
        table.put_item(Item=entry)
        table= dynamodb.Table(ShoppingCart)
        table.delete()
        PopulateTables.CreateShoppingCart(ShoppingCart)
        table= dynamodb.Table(Receipts)
        receipt=table.get_item(Key={'ReceiptId':len(List(Receipts))})
        return render_template('confirmation.html', data=receipt['Item'])
    else:
        return render_template('checkout.html', data=List(ShoppingCart))


def ManagePost(name,request):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table=dynamodb.Table(ShoppingCart)
    temp=dynamodb.Table("MyStore").get_item(Key={'ItemName':name})
    item=temp['Item']
    changed=False
    entry={'ItemName': name,'Amount': Decimal(request.form['count']),'price':Decimal(item['price']), 'TotalCost':Decimal(request.form['count'])*Decimal(item['price']) }
    table=dynamodb.Table(ShoppingCart)
    for i in List(ShoppingCart):
        if name == i['ItemName']:

            table.update_item(Key={'ItemName':name},UpdateExpression="set Amount=:a,TotalCost=:t",ExpressionAttributeValues={':a':i['Amount']+Decimal(request.form['count']),':t':i['TotalCost']+i['TotalCost']*Decimal(request.form['count'])})
            changed=True
    if not changed:
        table.put_item(Item=entry)
    table=dynamodb.Table("MyStore")
    entry=dynamodb.Table("MyStore").get_item(Key={'ItemName':name})
    table.update_item(Key={'ItemName':name},UpdateExpression="set stock=:s",ExpressionAttributeValues={':s':entry['Item']['stock']-Decimal(request.form['count'])})
    entry=dynamodb.Table("MyStore").get_item(Key={'ItemName':name})
    #print(ShoppingCart)
    #print(List(ShoppingCart),"\n")

def dateSort(e):
  return e["date"]

def priceSort(e):
    return e["SubTotal"]

@app.route('/buynow/<name>',methods=['POST'])
def BuyNow(name):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table=dynamodb.Table(ShoppingCart)
    temp=dynamodb.Table("MyStore").get_item(Key={'ItemName':name})
    item=temp['Item']
    changed=False
    entry={'ItemName': name,'Amount': Decimal(request.form['count']),'price':Decimal(item['price']), 'TotalCost':Decimal(request.form['count'])*Decimal(item['price']) }
    table=dynamodb.Table(ShoppingCart)
    for i in List(ShoppingCart):
        if name == i['ItemName']:
            table.update_item(Key={'ItemName':name},UpdateExpression="set Amount=:a,TotalCost=:t",ExpressionAttributeValues={':a':i['Amount']+Decimal(request.form['count']),':t':i['TotalCost']+i['TotalCost']*Decimal(request.form['count'])})
            changed=True
    if not changed:
        table.put_item(Item=entry)
    table=dynamodb.Table("MyStore")
    temp=dynamodb.Table("MyStore").get_item(Key={'ItemName':name})
    table.update_item(Key={'ItemName':name},UpdateExpression="set stock=:s",ExpressionAttributeValues={':s':temp['Item']['stock']-Decimal(request.form['count'])})
    temp=dynamodb.Table("MyStore").get_item(Key={'ItemName':name})
    return render_template('checkout.html', data=List(ShoppingCart))

@app.route('/delete',methods=['POST'])
def Delete():
    dynamodb=boto3.resource('dynamodb',endpoint_url="http://localhost:8000")
    table=dynamodb.Table(ShoppingCart)
    item=table.get_item(Key={'ItemName':request.form['Delete']})
    item=item['Item']
    store=dynamodb.Table('MyStore')
    old=store.get_item(Key={'ItemName':request.form['Delete']})
    old=old['Item']
    store.update_item(Key={'ItemName':request.form['Delete']},UpdateExpression="set stock=:s",ExpressionAttributeValues={':s':old['stock']+Decimal(item['Amount'])})
    table.delete_item(Key={'ItemName': request.form['Delete']})
    return render_template('checkout.html', data=List(ShoppingCart))

@app.route('/sortdate',methods=['POST'])
def SortDate():
    data=List(Receipts)
    data.sort(reverse=True,key=dateSort)
    return render_template('summary.html',receipts=data)

@app.route('/sortprice',methods=['POST'])
def SortPrice():
    data=List(Receipts)
    data.sort(reverse=True,key=priceSort)
    return render_template('summary.html',receipts=data)

def List(tableName):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    itemsInfo = dynamodb.Table(tableName).scan()
    return itemsInfo['Items']
