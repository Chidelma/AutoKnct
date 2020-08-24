from imports import *
from AUTO import *
from CRUD import * 
from TEXT import *

#db = firestore.Client()

conString = os.environ['conString']
client = MongoClient(conString)
colMong = client[os.environ['mongName']][os.environ['mongCol']]
cogClient = boto3.client('cognito-idp', 'ca-central-1')
mailClient = boto3.client('workmail', 'us-east-1')


def initRecords(event, context):

    dates = colMong.find({}, { "_id": 0, "Date": 1 }).distinct('Date')

    dates.sort(reverse=True)

    autoList = list(colMong.find({ 'Date' : dates[0] }).sort('Model'))

    newList = []

    for doc in autoList:

        if isinstance(doc['CYL'], str):
            newList.append(doc)
        else:
            currQuery = { "VIN" : doc['VIN'], "Date" : doc['Date'] }

            newValues = { "$set": { "CYL": None } }

            colMong.update_one(currQuery, newValues)

            newDoc = list(colMong.find({ "VIN" : doc['VIN'], "Date" : doc['Date'] }))

            newList.append(newDoc[0])

    return newList


def getAllUsers():

    return retrieveAllUsers()


def createUser(event, context):

    if createAUser(event) == "FAILED":
        return "FAILED"
    else:
        return "SUCCESS"


def searchQuery(event, context):

    results = list(colMong.find({ 'Model' : { '$regex' : event['query'] } }).sort('Model'))

    df = pd.DataFrame(results)

    df['Date'] = pd.to_datetime(df['Date'])

    df.index = df['Date']

    gk = df.resample('M').agg(['mean', 'count']).fillna(0).astype(int)

    gk.index = gk.index.strftime('%b %y')

    return {
        'Dates' : list(gk.index),
        'Prices' : list(gk['Price']['mean']),
        'Counts' : list(gk['Price']['count']),
        'Results' : results
    }


def filterResults(event, context):

    tempResults = []

    if event['filter']['startYear'] != '' and event['filter']['endYear'] == '':
        for auto in event['result']:
            if auto['Year'] >= event['filter']['startYear']:
                tempResults.append(auto)

    if event['filter']['endYear'] != '' and event['filter']['startYear'] == '':
        for auto in event['result']:
            if auto['Year'] <= event['filter']['endYear']:
                tempResults.append(auto)

    if event['filter']['endYear'] != '' and event['filter']['startYear'] != '':
        for auto in event['result']:
            if auto['Year'] >= event['filter']['startYear'] and auto['Year'] <= event['filter']['endYear']:
                tempResults.append(auto)
    
    if event['filter']['CYL'] != '':
        for auto in event['result']:
            if event['filter']['CYL'] in auto['CYL']:
                tempResults.append(auto)

    if event['filter']['Status'] != '':
        for auto in event['result']:
            if event['filter']['Status'] == auto['Status']:
                tempResults.append(auto)

    if event['filter']['startDate'] != '' and event['filter']['endDate'] == '':
        for auto in event['result']:
            if event['filter']['startDate'] <= auto['Date']:
                tempResults.append(auto)

    if event['filter']['endDate'] != '' and event['filter']['startDate'] == '':
        for auto in event['result']:
            if event['filter']['endDate'] >= auto['Date']:
                tempResults.append(auto)

    if event['filter']['endDate'] != '' and event['filter']['startDate'] != '':
        for auto in event['result']:
            if event['filter']['endDate'] >= auto['Date'] and event['filter']['startDate'] <= auto['Date']:
                tempResults.append(auto)

    if event['filter']['minMile'] != '' and event['filter']['maxMile'] == '':
        for auto in event['result']:
            if event['filter']['minMile'] <= auto['Mileage']:
                tempResults.append(auto)

    if event['filter']['maxMile'] != '' and event['filter']['minMile'] == '':
        for auto in event['result']:
            if event['filter']['maxMile'] >= auto['Mileage']:
                tempResults.append(auto)

    if event['filter']['maxMile'] != '' and event['filter']['minMile'] != '':
        for auto in event['result']:
            if event['filter']['maxMile'] >= auto['Mileage'] and event['filter']['minMile'] <= auto['Mileage']:
                tempResults.append(auto)

    if event['filter']['minBid'] != '' and event['filter']['maxBid'] == '':
        for auto in event['result']:
            if event['filter']['minBid'] <= auto['Price']:
                tempResults.append(auto)

    if event['filter']['maxBid'] != '' and event['filter']['minBid'] == '':
        for auto in event['result']:
            if event['filter']['maxBid'] >= auto['Price']:
                tempResults.append(auto)

    if event['filter']['maxBid'] != '' and event['filter']['minBid'] != '':
        for auto in event['result']:
            if event['filter']['maxBid'] >= auto['Price'] and event['filter']['minBid'] <= auto['Price']:
                tempResults.append(auto)

    df = pd.DataFrame(tempResults)
 
    df['Date'] = pd.to_datetime(df['Date'])

    df.index = df['Date']

    gk = df.resample('M').agg(['mean', 'count']).astype(int)

    gk.index = gk.index.strftime('%b %y')

    return {
        'Dates' : list(gk.index),
        'Prices' : list(gk['Price']['mean']),
        'Counts' : list(gk['Price']['count']),
        'Results' : tempResults
    }


def checkUser(event, context):
    userId = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(event['username'])))

    if retrieveUser(userId) != None:
        return retrieveUser(userId)
    else:
        return retrieveUser(createCUser(event))
        

def updateUser(event, context):

    return updateCUser(event)

def getEmailId(email):

    response = mailClient.list_users(
        OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c'
    )

    users = response['Users']
    userId = None

    for user in users:
        if user['Email'] == email:
            userId = user['Id']
            break

    return userId


def resetEmailPassword(event, context):

    return updateWorkmailPassword(event['email'], event['newPassword'])


def disableUser(event, context):

    cogClient.admin_disable_user(
        UserPoolId='ca-central-1_YslZwdQdK',
        Username=event['username']
    )

    if event['userType'][0] == 'A':

        adminUserId = getEmailId(event['email'])

        mailClient.deregister_from_work_mail(
            OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c',
            EntityId=adminUserId
        )

    return "SUCCESS"


def deleteUser(event, context):

    deleteUserCognito(event['username'])

    if event['userType'][0] == 'A':
        deleteUserWorkmail(event['email'])

    deleteCUser(event)

    return "SUCCESS"


def getGarageAutos(Garage):

    owned = []
    compared = []
    shared = []

    for comp in Garage['Compare']:
        compared.append(colMong.find_one({ '_id' : comp }))

    for share in Garage['Shared']:
        shared.append(colMong.find_one({ '_id' : share }))

    for own in Garage['Owned']:
        owned.append(colMong.find_one({ '_id' : own }))

    return {
        'owned' : owned,
        'compare' : compared,
        'shared' : shared
    }

def addToGarage(event, context):
    doc_ref = db.collection(event['type'].decode('utf-8')).document(event['uuid'].decode('utf'))

    if event['map'] == 'owned':
        doc_ref.update({u'Garage.Owned': firestore.ArrayUnion([event['ID'].decode('utf')])})
    if event['map'] == 'compared':
        doc_ref.update({u'Garage.Compare': firestore.ArrayUnion([event['ID'].decode('utf')])})
    if event['map'] == 'shared':
        doc_ref.update({u'Garage.Shared': firestore.ArrayUnion([event['ID'].decode('utf')])})

    return getGarageAutos(doc_ref.get().to_dict()['Garage'])

def removeAuto(event, context):
    doc_ref = db.collection(event['type'].decode('utf-8')).document(event['uuid'].decode('utf'))

    if event['map'] == 'owned':
        doc_ref.update({u'Garage.Owned': firestore.ArrayRemove([event['ID'].decode('utf')])})
    if event['map'] == 'compared':
        doc_ref.update({u'Garage.Compare': firestore.ArrayRemove([event['ID'].decode('utf')])})
    if event['map'] == 'shared':
        doc_ref.update({u'Garage.Shared': firestore.ArrayRemove([event['ID'].decode('utf')])})

    return getGarageAutos(doc_ref.get().to_dict()['Garage'])

def shareVehicle(event, context):
    doc_ref = db.collection(u'COMMENTS').document(event['vin'].decode('utf-8'))

    if doc_ref.get().to_dict() == None:

        comInfo = {
            u'userID' : event['userID'].decode('utf-8'),
            u'autoID' : event['autoID'].decode('utf-8'),
            u'date' : event['date'].decode('utf-8'),
            u'name' : event['name'].decode('utf-8'),
            u'text' : event['text'].decode('utf-8')
        }

        db.collection(u'COMMENTS').document(event['vin'].decode('utf-8')).set({
            u'vikComs' : [comInfo]
        })
    else:
        comInfo = {
            u'userID' : event['userID'].decode('utf-8'),
            u'autoID' : event['autoID'].decode('utf-8'),
            u'date' : event['date'].decode('utf-8'),
            u'name' : event['name'].decode('utf-8'),
            u'text' : event['text'].decode('utf-8')
        }

        doc_ref.update({u'vikComs': firestore.ArrayUnion([comInfo])})

    return doc_ref.get().to_dict()['vikComs']


def postComment(event, context):

    if(retreiveComments(event['vin']) != None):
        return updateComments(event)
    else:
        return createComment(event)


def getAnalytics(event, context):

    vin = event['vin']

    model = event['model']

    year = event['year']

    newGarage = []

    chartAxis = []

    df = pd.DataFrame(colMong.find({ "VIN": vin }).sort('Date'))

    autoCount = len(df.index)

    minBid = df['Price'].min() if df['Price'].min() != None else None

    maxBid = df['Price'].max() if df['Price'].max() != None else None

    avgBid = df['Price'].mean() if df['Price'].mean() != None else None

    for i in range(len(df.index)):
        auto = df.loc[i, :]

        newGarage.append({
            'Date' : auto['Date'],
            'Images' : auto['Images'] if 'Images' in auto else [],
            'Mileage' : auto['Mileage'],
            'Model' : auto['Model'],
            'CYL' : auto['CYL'],
            'Price' : auto['Price'],
            'Status' : auto['Status'],
            'VIN' : auto['VIN'],
            'Year' : auto['Year'],
            '_id' : auto['_id']
        })

        if auto['Price'] != None:
            chartAxis.append({ 'Date' : auto['Date'], 'Price' : auto['Price'] })
        else:
            chartAxis.append({ 'Date' : auto['Date'], 'Price' : 0 })

    prediction = predictSell(df)

    timeSpan = int(datetime.now().strftime("%Y")) - year

    if 'trailer' in model.lower() or timeSpan > 25 or 'motorcycle' in model.lower() or 'moped' in model.lower():
        extPrice = 'Unavailable'
    else:
        if prediction != 'Unavailable':
            avgExtPrice = getExtPrice(model, str(year))

            extPrice = int(avgExtPrice) - int(prediction)
        else:
            extPrice = getExtPrice(model, str(year))

    doc_ref = db.collection(u'COMMENTS').document(event['vin'].decode('utf-8'))

    if doc_ref.get().to_dict() == None:
        allComments = None
    else:
        allComments = doc_ref.get().to_dict()['vikComs']

    avgDetails = {
        'avgSalePrice' : int(prediction) if prediction != 'Unavailable' else 'Unavailable',
        'avgBidPrice' : 'Unavailable' if math.isnan(avgBid) else int(avgBid),
        'listGarage' : newGarage,
        'listChart' : chartAxis,
        'extData' : int(extPrice) if extPrice != 'Unavailable' else 'Unavailable',
        'maxBid' : 'Unavailable' if math.isnan(maxBid) else maxBid,
        'minBid' : 'Unavailable' if math.isnan(minBid) else minBid,
        'count' : autoCount,
        'comments' : allComments
    }

    return avgDetails

def predictSell(df):

    if df['Price'].isnull().any():
        prediction = predictionAlgorithm(df)
    else:
        prediction = avgSalePrice(df)

    return 'Unavailable' if prediction.empty else prediction['Price'].mean()


def avgSalePrice(df):

    for i in range(len(df.index)):
        modelArr = df.loc[i, :]['Model'].split()

        if len(modelArr) < 3:
            modelQuery = modelArr[0] + ' ' + modelArr[1]
        else:
            modelQuery = modelArr[0] + ' ' + modelArr[1] + ' ' + modelArr[2]

        results = list(colMong.find({ 
                    "$and" : [
                        { "Model" : { "$regex" : modelQuery }}, 
                        { "Price" : { '$ne' : None } }, 
                        { "Status" : df.loc[i, :]['Status'] }, 
                        { "CYL" : df.loc[i, :]['CYL'] }, 
                        { "Year" : df.loc[i, :]['Year'] }, 
                        { "VIN" : { '$ne' : df.loc[i, :]['VIN'] } }
                    ]
                }))

    results = pd.DataFrame(results)

    if len(results.index) == 0:

        for i in range(len(df.index)):
            modelArr = df.loc[i, :]['Model'].split()

            if len(modelArr) < 3:
                modelQuery = modelArr[0] + ' ' + modelArr[1]
            else:
                modelQuery = modelArr[0] + ' ' + modelArr[1] + ' ' + modelArr[2]

            results = list(colMong.find({ 
                        "$and" : [
                            { "Model" : { "$regex" : modelQuery }}, 
                            { "Price" : { '$ne' : None } }, 
                            { "Status" : df.loc[i, :]['Status'] }, 
                            { "Year" : df.loc[i, :]['Year'] }, 
                            { "VIN" : { '$ne' : df.loc[i, :]['VIN'] } }
                        ]
                    }))

    results = pd.DataFrame(results)

    if len(results.index) == 0:

        for i in range(len(df.index)):
            modelArr = df.loc[i, :]['Model'].split()

            if len(modelArr) < 3:
                modelQuery = modelArr[0] + ' ' + modelArr[1]
            else:
                modelQuery = modelArr[0] + ' ' + modelArr[1] + ' ' + modelArr[2]

            results = list(colMong.find({ 
                        "$and" : [
                            { "Model" : { "$regex" : modelQuery }}, 
                            { "Price" : { '$ne' : None } }, 
                            { "Year" : df.loc[i, :]['Year'] }, 
                            { "VIN" : { '$ne' : df.loc[i, :]['VIN'] } }
                        ]
                    }))

    results = pd.DataFrame(results)

    if len(results.index) == 0:

        for i in range(len(df.index)):
            modelArr = df.loc[i, :]['Model'].split()

            if len(modelArr) < 3:
                modelQuery = modelArr[0] + ' ' + modelArr[1]
            else:
                modelQuery = modelArr[0] + ' ' + modelArr[1] + ' ' + modelArr[2]

            results = list(colMong.find({ 
                        "$and" : [
                            { "Model" : { "$regex" : modelQuery }}, 
                            { "Price" : { '$ne' : None } }, 
                            { "Status" : df.loc[i, :]['Status'] }, 
                            { "VIN" : { '$ne' : df.loc[i, :]['VIN'] } }
                        ]
                    }))

    results = pd.DataFrame(results)

    if len(results.index) == 0:

        for i in range(len(df.index)):
            modelArr = df.loc[i, :]['Model'].split()

            if len(modelArr) < 3:
                modelQuery = modelArr[0] + ' ' + modelArr[1]
            else:
                modelQuery = modelArr[0] + ' ' + modelArr[1] + ' ' + modelArr[2]

            results = list(colMong.find({ 
                        "$and" : [
                            { "Model" : { "$regex" : modelQuery }}, 
                            { "Price" : { '$ne' : None } }, 
                            { "VIN" : { '$ne' : df.loc[i, :]['VIN'] } }
                        ]
                    }))

    return pd.DataFrame(results)


def predictionAlgorithm(df):
    
    unSold = df.loc[0, :] if len(df.index) == 1 else df.loc[len(df.index) - 1, :]

    modelArr = unSold['Model'].split() 

    if len(modelArr) <= 3:
        modelQuery = modelArr[0] + ' ' + modelArr[1]
    else:
        modelQuery = modelArr[0] + ' ' + modelArr[1] + ' ' + modelArr[2]

    prediction = list(colMong.find({ 
                    "$and" : [
                        { "Model" : { "$regex" : modelQuery }}, 
                        { "Price" : { '$ne' : None } }, 
                        { "Status" : unSold['Status'] }, 
                        { "CYL" : unSold['CYL'] }, 
                        { "Year" : unSold['Year'] } 
                    ]
                }))

    if prediction == None or prediction == []:
        prediction = list(colMong.find({ 
                    "$and" : [
                        { "Model" : { "$regex" : modelQuery }}, 
                        { "Price" : { '$ne' : None } }, 
                        { "Status" : unSold['Status'] }, 
                        { "Year" : unSold['Year'] } 
                    ]
                }))

    if prediction == None or prediction == []:
        prediction = list(colMong.find({ 
                    "$and" : [
                        { "Model" : { "$regex" : modelQuery }}, 
                        { "Price" : { '$ne' : None } },  
                        { "Year" : unSold['Year'] } 
                    ]
                }))

    if prediction == None or prediction == []:
        prediction = list(colMong.find({ 
                    "$and" : [
                        { "Model" : { "$regex" : modelQuery }}, 
                        { "Price" : { '$ne' : None } }, 
                        { "Status" : unSold['Status'] }
                    ]
                }))

    if prediction == None or prediction == []:
        prediction = list(colMong.find({ 
                    "$and" : [
                        { "Model" : { "$regex" : modelQuery }}, 
                        { "Price" : { '$ne' : None } }
                    ]
                }))

    return pd.DataFrame(prediction)
    

def getExtPrice(model, year):

    modelArr = model.split()

    year = str(year)

    try:
        if len(modelArr) == 3 and (len(modelArr[2]) == 2 or len(modelArr[2]) == 3):
            url = "https://www.kijiji.ca/b-cars-vehicles/canada/" + year + "-" + modelArr[0] + "-" + modelArr[1] + "-" + modelArr[2] +"/k0c27l0?ad=offering&price=1000__100000"
        else:
            url = "https://www.kijiji.ca/b-cars-vehicles/canada/" + year + "-" + modelArr[0] + "-" + modelArr[1] +"/k0c27l0?ad=offering&price=1000__100000"
            
        page = requests.get(url.lower())

        doc = lh.fromstring(page.content)

        pricelist = doc.xpath('//div[@class="price"]')

        prices = []

        for price in pricelist:
            price = " ".join(price.text_content().split())
            if price.replace('$', '').replace(',', '').replace('.00','').isdigit():
                prices.append(int(price.replace('$', '').replace(',', '').replace('.00','')))

        return int(sum(prices) / len(prices))
    except:
        try:
            if len(modelArr) == 3 and (len(modelArr[2]) == 2 or len(modelArr[2]) == 3):
                url = "https://www.autotrader.ca/cars/" + modelArr[0] + "/" + modelArr[1] + "%20" + modelArr[2] + "/" + year + "/?rcp=100&sts=Used"
            else:
                url = "https://www.autotrader.ca/cars/" + modelArr[0] + "/" + modelArr[1] + "/" + year + "/?rcp=100&sts=Used"
                
            page = requests.get(url.lower())

            doc = lh.fromstring(page.content)

            pricelist = doc.xpath('//span[@class="price-amount"]')

            prices = []

            for price in pricelist:
                price = " ".join(price.text_content().split())
                if price.replace('$', '').replace(',', '').replace('.00','').isdigit():
                    prices.append(int(price.replace('$', '').replace(',', '').replace('.00','')))

            priceAge = int(sum(prices) / len(prices))

            if priceAge > 30000:
                url = "https://www.autotrader.ca/cars/" + modelArr[0] + "/" + modelArr[1] + "/" + year + "/?rcp=100&sts=Used"
                    
                page = requests.get(url.lower())

                doc = lh.fromstring(page.content)

                pricelist = doc.xpath('//span[@class="price-amount"]')

                prices = []

                for price in pricelist:
                    price = " ".join(price.text_content().split())
                    if price.replace('$', '').replace(',', '').replace('.00','').isdigit():
                        prices.append(int(price.replace('$', '').replace(',', '').replace('.00','')))

                return int(sum(prices) / len(prices))
            else:
                return int(sum(prices) / len(prices))

        except:
            if len(modelArr) == 3 and (len(modelArr[2]) == 2 or len(modelArr[2]) == 3):
                url = "https://www.kijijiautos.ca/cars/" + modelArr[0] + "/" + modelArr[1] + "-" + modelArr[2] + "/" + year + "/"
            else:
                url = "https://www.kijijiautos.ca/cars/" + modelArr[0] + "/" + modelArr[1] + "/" + year + "/"
                
            page = requests.get(url.lower())

            doc = lh.fromstring(page.content)

            pricelist = doc.xpath('//span[@class="_257rsiOLZRw2SUP41j3TiB _2EdRVi2tLqR7VPkJ2yR6Zx QVJux59ueO-M7o0DZZ6Vx _14Nqyg9Gv-h-nJ_lZalHW_"]')

            prices = []

            for price in pricelist:
                price = " ".join(price.text_content().split())
                if price.replace('$', '').replace(',', '').replace('.00','').isdigit():
                    prices.append(int(price.replace('$', '').replace(',', '').replace('.00','')))

            return int(sum(prices) / len(prices)) if len(prices) != 0 else 'Unavailable'