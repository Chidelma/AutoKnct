from imports import *
from USER import *
from AUTO import *
from TEXT import *


db = firestore.Client()
conString = os.environ['conString']
client = MongoClient(conString)
colMong = client[os.environ['mongName']][os.environ['mongCol']]

cogClient = boto3.client('cognito-idp', 'ca-central-1')
mailClient = boto3.client('workmail', 'us-east-1')


def createUserWorkmail(email, fullName, tempPassword):

    res = mailClient.create_user(
        OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c',
        Name=email,
        DisplayName=fullName,
        Password=tempPassword
    )

    mailClient.register_to_work_mail(
        OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c',
        EntityId=res['UserId'],
        Email=email
    )

    return "SUCCESS"


def createUserCognito(name, email, tempPassword, username, group):

    cogClient.admin_create_user(
        UserPoolId='ca-central-1_YslZwdQdK',
        Username=username,
        UserAttributes=[
            {
                'Name': 'name',
                'Value': name
            },
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name' : 'email_verified',
                'Value' : 'true'
            }
        ],
        ValidationData=[],
        TemporaryPassword=tempPassword,
        ForceAliasCreation=False,
        MessageAction='SUPPRESS',
        DesiredDeliveryMediums=['EMAIL']
    )

    cogClient.admin_add_user_to_group(
        UserPoolId='ca-central-1_YslZwdQdK',
        Username=username,
        GroupName=group
    )

    return "SUCCESS"


def createCUser(event):

    newUser = Customer(event['name'], event['email'], event['username'], None)

    db.collection(u'USERS').document(newUser.UserId).set({
        u'Picture' : newUser.Picture,
        u'Name' : newUser.Name,
        u'Username' : newUser.Username,
        u'Email' : newUser.Email,
        u'Garage' : {
            u'Shared' : [],
            u'Compare' : [],
            u'Owned' : []
        },
        u'Type' : newUser.Type
    })

    return newUser.UserId


def createBUser(event):

    newUser = Business(event['name'], event['email'], event['username'], event['id'], event['businessName'], None)

    db.collection(u'USERS').document(newUser.UserId).set({
        u'Picture' : newUser.Picture,
        u'Name' : newUser.Name,
        u'Business Name' : newUser.BusinessName,
        u'Customer ID' : newUser.CustomerId,
        u'Username' : newUser.Username,
        u'Email' : newUser.Email,
        u'Garage' : {
            u'Auction' : [],
            u'Shared' : [],
            u'Compare' : [],
            u'Owned' : []
        },
        u'Type' : newUser.Type
    })

    return newUser.UserId


def createAUser(event):

    if event['midName'] != '':
        username = event['lastName'].lower() + event['firstName'][0].lower() + event['midName'][0].lower()
        email = event['lastName'].lower() + event['firstName'][0].lower() + event['midName'][0].lower() + '@autoknct.com'
        fullName = event['firstName'] + ' ' + event['midName'][0] + '. ' + event['lastName']
    else:
        username = event['lastName'].lower() + event['firstName'][0].lower()
        email = event['lastName'].lower() + event['firstName'][0].lower() + '@autoknct.com'
        fullName = event['firstName'] + ' ' + event['lastName']

    tempPassword = event['lastName'] + event['dob']

    newUser = Admin(fullName, email, username, event['dob'], None, event['role'])

    db.collection(u'USERS').document(newUser.UserId).set({
        u'Picture' : newUser.Picture,
        u'Name' : newUser.Name,
        u'D.O.B' : newUser.Dob,
        u'Role' : newUser.Role,
        u'Username' : newUser.Username,
        u'Email' : newUser.Email,
        u'Garage' : {
            u'Shared' : [],
            u'Compare' : [],
            u'Owned' : []
        },
        u'Type' : newUser.Type
    })

    userWorkmail = createUserWorkmail(newUser.Email, newUser.Name, tempPassword)

    userCognito = createUserCognito(newUser.Name, newUser.Email, tempPassword, newUser.Username, event['group'])

    if userWorkmail == "SUCCESS" and userCognito == "SUCCESS":
        return newUser.UserId
    else:
        return "FAILED"


def createComment(event):

    if event['autoID'] != None:
        comment = Text(event['id'], event['name'], event['date'], event['text'], event['autoID'], event['vin'])
    else:
        comment = Text(event['id'], event['name'], event['date'], event['text'], None, event['vin'])

    newText = {
        u'userID' : comment.userID,
        u'autoID' : comment.auto,
        u'date' : comment.date,
        u'name' : comment.name,
        u'text' : comment.text
    }

    db.collection(u'COMMENTS').document(comment.VIN).set({
        u'autoComs' : [newText]
    })

    return retreiveComments(comment.VIN)


def retrieveWorkmailId(email):

    res = mailClient.list_users(
        OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c'
    )

    users = res['Users']
    userId = None

    for user in users:
        if user['Email'] == email:
            userId = user['Id']
            break

    return userId


def retreiveComments(VIN):

    doc_ref = db.collection(u'COMMENTS').document(VIN).get().to_dict()

    if doc_ref != None:
        return doc_ref['autoComs']
    else:
        return None


def retrieveAuto(ID):

    return Auto(colMong.find_one({ '_id' : ID }))


def retrieveUserGarage(Garage, Type):

    owned = []
    compared = []
    shared = []
    auction = []

    for comp in Garage['Compare']:
        compared.append(retrieveAuto(comp))

    for share in Garage['Shared']:
        shared.append(retrieveAuto(share))

    for own in Garage['Owned']:
        owned.append(retrieveAuto(own))

    if Type == 'BUSER':
        for auct in Garage['Auction']:
            auction.append(retrieveAuto(auct))

    return {
        'owned' : owned,
        'compare' : compared,
        'shared' : shared,
        'auction' : auction
    }


def retrieveUser(ID):

    user = db.collection(u'USERS').document(ID).get().to_dict()

    if user != None:

        return {
            'id' : ID,
            'user' : user,
            'garage' : retrieveUserGarage(user['Garage'], user['Type'])
        }
    else:
        return None


def retrieveAllUsers():

    allUsers = []

    users = db.collection(u'USERS').stream()

    for user in users:
        currUser = user.to_dict()
        currUser['id'] = user.id

        res = cogClient.admin_get_user(
            UserPoolId='ca-central-1_YslZwdQdK',
            Username=currUser['Username']
        )

        currUser['Status'] = res['UserStatus']
        currUser['Enabled'] = res['Enabled']
        allUsers.append(currUser)

    return allUsers


def updateWorkmailPassword(email, newPassword):

    userId = retrieveWorkmailId(email)

    mailClient.reset_password(
        OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c',
        UserId=userId,
        Password=newPassword
    )

    return "SUCCESS"


def updateComments(event):

    doc_ref = db.collection(u'COMMENTS').document(event['vin'].decode('utf-8')).get().to_dict()

    comment = Text(event['id'], event['name'], event['date'], event['text'], event['autoID'], event['vin'])

    newText = {
        u'userID' : comment.userID,
        u'autoID' : comment.auto,
        u'date' : comment.date,
        u'name' : comment.name,
        u'text' : comment.text
    }

    doc_ref.update({u'autoComs': firestore.ArrayUnion([newText])})

    return doc_ref['autoComs']


def updateCUser(event):

    if retrieveUser(event['id']) != None:

        db.collection(u'USERS').document(event['id'].decode('utf-8')).update({
            u'Name' : event['name'].decode('utf-8'),
            u'Email' : event['email'].decode('utf-8'),
            u'Picture' : event['picture']
        })

        return "SUCCESS: User Has Been Updated"
    else:
        return "FAILED: User Doesn't Exist!"


def deleteCUser(event):

    userId = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(event['username'])))

    if retrieveUser(userId) != None:

        db.collection(u'USERS').document(userId.decode('utf-8')).delete()
    
        return "SUCCESS: User Has Been Deleted"
    else:
        return "FAILED: User Doesn't Exist!"


def deleteUserWorkmail(email):

    userId = retrieveWorkmailId(email)

    client.deregister_from_work_mail(
        OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c',
        EntityId=userId
    )

    client.delete_user(
        OrganizationId='m-38a3cf9518b5441e877a0115d02c6b2c',
        UserId=userId
    )


def deleteUserCognito(username):

    client.admin_delete_user(
        UserPoolId='ca-central-1_YslZwdQdK',
        Username=username
    )