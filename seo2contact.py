import requests
import json
import urllib
import pandas as pd
import streamlit as st
import re


def get_contacts():
    # This example displays how to get all contacts from a HubID and paginate through them using the 'offset' parameter.
    # The end result is a python list containing all parsed contacts. 

    count = 500
    contact_list = []
    get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
    parameter_dict = {'count': count, 'property':"seoname"}
    headers = {
        'Authorization': 'Bearer '+bearer_token
    }
#    print("in get contacts")
    # Paginate your request using offset
    has_more = True
    while has_more:
        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = get_all_contacts_url + parameters
        r = requests.get(url= get_url, headers = headers)
        response_dict = json.loads(r.text)
        has_more = response_dict['has-more']
        contact_list.extend(response_dict['contacts'])
        parameter_dict['vidOffset']= response_dict['vid-offset']

#        print('loop finished')

    list_length = len(contact_list) 

    print("You've successfully parsed through {} contact records and added them to a list".format(list_length))
    return(contact_list)

def get_companies():

    count = 500
    company_list = []
    get_all_companies_url = "https://api.hubapi.com/companies/v2/companies/paged?&properties=seoName&properties=name&properties=brand_name&"

    parameter_dict = {'count': count}#, 'properties':"seoName", 'properties':"name", 'properties':"brand_name"}
    headers = {
        'Authorization': 'Bearer '+bearer_token
    }

    # Paginate your request using offset
    has_more = True
    while has_more:
        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = get_all_companies_url + parameters
        r = requests.get(url= get_url, headers = headers)
        response_dict = json.loads(r.text)
#        print(r.text)
        has_more = response_dict['has-more']
        company_list.extend(response_dict['companies'])
        parameter_dict['offset']= response_dict['offset']

    print('loop finished')

    list_length = len(company_list) 

    print("You've successfully parsed through {} companies and added them to a list".format(list_length))
    return(company_list)



def get_deals(bearer_token):
    # This example displays how to get all contacts from a HubID and paginate through them using the 'offset' parameter.
    # The end result is a python list containing all parsed contacts. 

    count = 500
    deal_list = []
    get_all_deals_url = "https://api.hubapi.com/deals/v1/deal/paged?"
    parameter_dict = {'count': count, 'properties':'dealname'}
    headers = {
        'Authorization': 'Bearer '+bearer_token
    }

    # Paginate your request using offset
    has_more = True
    while has_more:
        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = get_all_deals_url + parameters
        r = requests.get(url= get_url, headers = headers)
        response_dict = json.loads(r.text)
        has_more = response_dict['hasMore']
        deal_list.extend(response_dict['deals'])
        parameter_dict['offset']= response_dict['offset']


    print('loop finished')

    list_length = len(deal_list) 

    print("You've successfully parsed through {} deals and added them to a list".format(list_length))
    return(deal_list)

def get_contact_byID(contactID):
    url = "https://api.hubapi.com/contacts/v1/contact/vid/"+contactID+"/profile"
    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + bearer_token
        }

    r = requests.get(url = url, headers = headers)
    return(json.loads(r.text))


def get_contacts_for_company(company):
    contact_list=[]
    url = "https://api.hubapi.com/crm/v4/objects/company/"+str(company)+"/associations/contact"

    querystring = {"limit":"100"}

    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + bearer_token
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    r=json.loads(response.text)
#    print(r)
    for val in r['results']:
#        print(val)
        contact_list.append(val["toObjectId"])
    return(contact_list)

def get_emailaddress_for_contact(contactId):
    import requests

    url = "https://api.hubapi.com/crm/v4/objects/contact/"+contactId+"/associations/email"

    querystring = {"limit":"500"}

    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + bearer_token
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    r = json.loads(response.text)
    email_list = []
    for val in r['results']:
        email_list.append(val["toObjectId"])
    return(email_list)

def get_engagements(bearer_from):
    get_all_engagements_url = "https://api.hubapi.com/engagements/v1/engagements/paged?"
    count=5

    engagement_list=[]
    parameter_dict = {'count': count}
    headers = {
        'Authorization': 'Bearer '+bearer_from
    }

    has_more = True
    while has_more:
        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = get_all_engagements_url + parameters
        r = requests.get(url= get_url, headers = headers)
        response_dict = json.loads(r.text)
#        print(response_dict)
        has_more = response_dict['hasMore']
        engagement_list.extend(response_dict['results'])
        parameter_dict['offset']= response_dict['offset']

    list_length = len(engagement_list) 
    print("You've successfully parsed through {} engagements and added them to a list".format(list_length))

    return(engagement_list)

def post_engagement(bearer_token, payload, file_object):
    post_engagement_url = "https://api.hubapi.com/engagements/v1/engagements"

    headers = {
            'Authorization': 'Bearer '+bearer_token,
            'Content-Type': "application/json",
        }

    response = requests.request("POST", post_engagement_url, data=json.dumps(payload), headers=headers)
    file_object.write(response.text)

def delete_engagement(engagementId, bearer_token):

    print("deleting engagement", engagementId)
    url = "http://api.hubapi.com/engagements/v1/engagements/"+str(engagementId)
    print("url", url)
    headers = {
            'Authorization': 'Bearer '+bearer_token,
        }
    response = requests.request("DELETE", url, headers=headers)
    print(response)
    return

def get_email(contact):
    email = []
#    print(contact)
    for identity in contact["identity-profiles"][0]["identities"]:
        if identity['type']=='EMAIL':
#            print(identity)
            if 'is-primary' in identity:
                email.append(identity['value'])
    return(email)

def upload_note(bearer_token, note):
    url = "https://api.hubapi.com/engagements/v1/engagements"
#    print(note)
    payload = json.dumps({
        "engagement": {
            "active": 'true',
            "ownerId": int(note["owner"]),
            "type": "NOTE",
            "timestamp": note["timestamp"]
        },
        "associations": {
            "contactIds": note["contacts"],
            "companyIds": note["companies"],
            "dealIds": note["deals"],
            "ownerIds": [ ]
        },
        # "attachments": [
        #     {
        #         "id": 4241968539
        #     }
        # ],
        "metadata": {
            "body": note["body"]
        }
        })  

    headers = {
            'Authorization': 'Bearer '+bearer_token,
            'Content-Type': "application/json",
        }
    response = requests.request("POST", url, data=payload, headers=headers)#, params=querystring)

    print("RESPONSE", response.text)


def upload_meeting(bearer_token, meeting):
    print("MEETING")
    print(meeting)
    url = "https://api.hubapi.com/engagements/v1/engagements"
#    print(note)
    payload = json.dumps({
        "engagement": {
            "active": 'true',
            "ownerId": meeting["owner"],
            "type": "MEETING",
            "timestamp": meeting["timestamp"]
        },
        "associations": {
            "contactIds": meeting["contacts"],
            "companyIds": meeting["companies"],
            "dealIds": meeting["deals"],
            "ownerIds": [ ]
        },
        # "attachments": [
        #     {
        #         "id": 4241968539
        #     }
        # ],
        "metadata": {
            "body": meeting["body"],
            "startTime": meeting["startTime"],
            "endTime": meeting["endTime"],
            "title": meeting["Subject"],
            "internalMeetingNotes" : meeting["notes"]
        }
        })  

    headers = {
            'Authorization': 'Bearer '+bearer_token,
            'Content-Type': "application/json",
        }
    response = requests.request("POST", url, data=payload, headers=headers)#, params=querystring)

    print("RESPONSE", response.text)


def upload_call(bearer_token, call):
    url = "https://api.hubapi.com/engagements/v1/engagements"
#    print(note)
    payload = json.dumps({
        "engagement": {
            "active": 'true',
            "ownerId": call["owner"],
            "type": "CALL",
            "timestamp": call["timestamp"]
        },
        "associations": {
            "contactIds": call["contacts"],
            "companyIds": call["companies"],
            "dealIds": call["deals"],
            "ownerIds": [ ]
        },
  
        "metadata": {      

            "toNumber" : call["toNumber"],
            "fromNumber" : call["fromNumber"],
            "status" : "COMPLETED",
            "durationMilliseconds" : call["duration"],
            "body" : call["body"]


        }
        })  

    headers = {
            'Authorization': 'Bearer '+bearer_token,
            'Content-Type': "application/json",
        }
    response = requests.request("POST", url, data=payload, headers=headers)#, params=querystring)

    print("RESPONSE", response.text)

def upload_email(bearer_token, email):
    url = "https://api.hubapi.com/engagements/v1/engagements"
#    print(note)
    payload = json.dumps({
        "engagement": {
            "active": 'true',
            "ownerId": email["owner"],
            "type": "EMAIL",
            "timestamp": email["timestamp"]
        },
        "associations": {
            "contactIds": email["contacts"],
            "companyIds": email["companies"],
            "dealIds": email["deals"],
            "ownerIds": [ ]
        },
        # "attachments": [
        #     {
        #         "id": 4241968539
        #     }
        # ],
        "metadata": {
            "from": {
                "email": "",
                "firstName": "",
                "lastName": ""
            },
            "to": [
            {
                "email": ""
            }
            ],
            "cc": [],
            "bcc": [],
            "subject": email["body"],
            "html": "",
            "text": ""
        }
        })  

    headers = {
            'Authorization': 'Bearer '+bearer_token,
            'Content-Type': "application/json",
        }
    response = requests.request("POST", url, data=payload, headers=headers)#, params=querystring)

    print("RESPONSE", response.text)

def create_ids_dict(contacts_origin, contacts_new):
    #create lookup dictionary from contact ID in old account to contact ID in new account
    ids_dict = {}
    for contact_old in contacts_origin:
    #    print("\n\n")
        email_old= get_email(contact_old)
        for contact_new in contacts_new:
            email_new = get_email(contact_new)
            if email_old == email_new:
                ids_dict[contact_old['vid']] = contact_new['vid']
    return(ids_dict)


def copy_engagements(bearer_from, bearer_to, ids_dict, owner_dict, do_update):
    old_engage = get_engagements(bearer_from)
    new_engage = get_engagements(bearer_to)
    print("New engagements, old engagements", len(new_engage), len(old_engage))
    uniq_existing = []
    for activity in new_engage:
        engageunique =  make_unique(activity)
        uniq_existing.append(engageunique)
    count=0
    count_updated = 0
    for engage in old_engage:
        #print("engage before", engage)
        uniquename = make_unique(engage)
#        print("initial unique name", uniquename)
        #swap out the contact id in the unique name
        oldcontacts = engage['associations']['contactIds']
        try:
            newcontacts_str = "".join([str(ids_dict[x]) for x in oldcontacts])
        except:
            print("no contact for old contact ", oldcontacts)
            continue
        oldcontacts_str = "".join([str(x) for x in oldcontacts])

        uniquename = uniquename.replace(oldcontacts_str, newcontacts_str)

        if uniquename in uniq_existing:
#            print("already exists")
            count+=1
            continue
        count_updated+=1
        print("old contacts", oldcontacts_str)
        print("new contacts", newcontacts_str)
        print("new uniquename", uniquename)
#        print("new engagement", engage)
#        ans = update = input("update?")
#        if ans.lower()!='y':
#            continue
        engage['engagement'].pop('id')
        engage['engagement'].pop('portalId')
        engage['engagement'].pop('createdAt')
        engage['engagement'].pop('lastUpdated')
        try:
            engage['engagement'].pop('createdBy')
        except:
            pass
        try:
            engage['engagement'].pop('modifiedBy')
        except:
            pass
        try:
            engage['engagement'].pop('bodyPreviewIsTruncated')
        except:
            pass
        engage['engagement']['companyIds'] = []
        engage['associations']['companyIds'] = []# TODOcompany_dict[engage['associations']['companyIds']]
        engage['associations']['dealIds'] = []# TODOdeal_dict[engage['associations']['dealIds']]
        if engage['engagement']['active'] == True:
            engage['engagement']['active'] = 'true'
        else:
            engage['engagement']['active'] = 'false'
        engage['engagement']['ownerId'] = owner_dict[engage['engagement']['ownerId']]
        newids=[]
        for id in engage["associations"]['contactIds']:
            if id in ids_dict:
                newids.append(ids_dict[id])
            else:
                print("need to move over", id)
    #    print("newids", newids)
        engage['associations']['contactIds'] = newids
#        print("after", engage)
#        input("next?")
        file_object = open('log.txt', 'w')
        if do_update:
            post_engagement(bearer_to, engage, file_object)
        file_object.close()
    print("already good", count)
    print("updated ", count_updated)
    return

def sync_engagements(bearer_from, bearer_to, owner_dict, do_update):
    origin = get_contacts(bearer_from)
    new = get_contacts(bearer_to)

    ids_dict = create_ids_dict(origin, new)

    copy_engagements(bearer_from, bearer_to, ids_dict, owner_dict, do_update)


def get_contact_owners(bearer):
    url = "https://api.hubapi.com/contacts/v1/search/query?"


    contacts_wowners = []
 
    headers = {
        'Authorization': 'Bearer '+bearer
    }
    parameter_dict = {'property':'hubspot_owner_id'}
    offset=True
    # Paginate your request using offset
    has_more = True
    while has_more:

        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = url + parameters
#        print("get_url", get_url)
        r = requests.get(url= get_url, headers = headers)
        response_dict = json.loads(r.text)

        contacts_wowners.extend(response_dict['contacts'])
        has_more=response_dict['has-more']
        parameter_dict['offset']= response_dict['offset']

    print('loop finished')

    list_length = len(contacts_wowners) 

    contact_owners = {}
    for contact in contacts_wowners:
        id = contact['vid']
        print('id', id)
        print(contact['properties'])
        if 'hubspot_owner_id' in contact['properties']:
            owner = contact['properties']['hubspot_owner_id']['value']
        else:
            owner = 0
        print('owner', owner)
        contact_owners[id] = owner

    return contact_owners

def copy_contact_owners(bearer_from, bearer_to, ids_dict):
    #requires:
    #bearer_from: bearer token of the account we're pulling from
    #ids_dict: dictionary linking old account contact ids to new contact ids

    old_owners = get_contact_owners(bearer_from)
    new_owners = {}

    for contactid in ids_dict:
        print(contactid)
        print(ids_dict[contactid])
        old_contactID = ids_dict[contactid]
        print(old_contactID)
        try:
            old_ownerID = old_owners[old_contactID]
            new_ownerid = lookup_HSowner(oldid = old_ownerID)
            new_owners[contactid] = new_ownerid
        except:
            print("owner for user ", contactid, "not found")
    update_contact_owners(bearer_to, new_owners)


    return

def update_contact_owners(bearer, new_owners):

    for id in new_owners:
        url ='https://api.hubapi.com/contacts/v1/contact/vid/'+str(id)+'/profile'
        headers = {
        'Authorization': 'Bearer '+bearer
        }
        headers['Content-Type']= 'application/json'

        data=json.dumps({ "properties": 
            [{
                "property": "hubspot_owner_id",
                "value": new_owners[id]
            },
            ]
        })

        r = requests.post(data=data, url=url, headers=headers)

        print(r.status_code)

def lookup_HSowner(name="", oldid="", newid=""):
    '''if name is defined, will return old and new ids for that name
    if no name, but oldid, will return new user id
    if no name, no oldid, but newid, will return old user id'''
    HS_owner_ids = {"Amanda Melendez":{"new": 27529488, "old":11036324}, 
    "Kymry Gotwald":{"new":27529490, "old":12517443},
    "Mauricio Rezende":{"new":27529487, "old":10950702},
    "Melissa Martin":{"new":25817642, "old":11257715}
    }

    if name:
        return (HS_owner_ids[name])
    elif oldid:
        for owner in HS_owner_ids:
            if owner['old'] == oldid:
                return owner['new']
    elif newid:
        for owner in HS_owner_ids:
            if owner['new'] == newid:
                return owner['old']
    return

        

    #contacts = get_contacts(bearer_token)
#HS_user_ids = [[28031262, "Ben Aston"],
#        [10637926, "Alysha Reinard"],
#        [28031267, "Adam"],
#        [28149098, "Joe"],
#        [28029255, "Amelia Yau"],
#        [28029251, "Isobel Thompson"],
#        [27610317, "Matt Brazil"],
#        [27967698, "David Cook"]]

def read_notes_csv():
    notes= pd.read_csv("./Pipedrive files/notes-13576130-29.csv")
    

    print(notes)
    return(notes)



def read_activities_csv():
    activities= pd.read_csv("./Pipedrive files/activities-13576130-28.csv")
    
    activities.fillna("", inplace=True)
    print(activities)
    return(activities)

def read_people_csv():
    people=pd.read_csv("./Pipedrive files/people-13576130-13.csv")
    print(people)
    return(people)


def match_contacts(df_orig, list_new):
    orig_HSid = []
    for i in range(len(df_orig)):
#        print("Person ", df_orig.Name[i])
#        print("Email ", df_orig.Email[i])
        email = df_orig.Email[i]
        HSid = ""
        for contact in list_new:
#            print("\n",contact["identity-profiles"])
#            print("\n",contact["identity-profiles"][0]["identities"])
            if contact["identity-profiles"][0]["identities"][0]['type'] == "EMAIL":
                contact_email = contact["identity-profiles"][0]["identities"][0]['value']
                if contact_email == email:

                    HSid = contact["identity-profiles"][0]['vid']
#                    print("HSid is ", HSid)
        orig_HSid.append(HSid)
    return orig_HSid
            

def match_contacts_byname(df_orig, list_new):
    print(df_orig)
    orig_HSid = []
    for i in range(len(df_orig)):
#        print("Person ", df_orig.Name[i])
#        print("Email ", df_orig.Email[i])
        orig_name = df_orig[i]
#        print("orig_name: ",orig_name)
        if orig_name == "":
            orig_HSid.append([])
            continue
        HSid = []
        for contact in list_new:
#            print("\n",contact)
#            print("\n",contact["identity-profiles"][0]["identities"])
            try:
                HSname = contact['properties']['firstname']['value'] + ' ' + contact['properties']['lastname']['value']
#                print("Name is ", HSname)
            except:

                continue

            if orig_name == HSname:

                HSid.append(int(contact["identity-profiles"][0]['vid']))
#                print("HSid is ", HSid)
        if HSid == []:
            orig_HSid.append(["NM + "+str(orig_name)])
        else:
            orig_HSid.append(HSid)
    return orig_HSid
            


def match_companies_byname(df_orig, list_new):
    orig_HSid = []
    for i in range(len(df_orig)):
#        print("Person ", df_orig.Name[i])
#        print("Email ", df_orig.Email[i])
        orig_name = df_orig[i]
        if orig_name == "":
            orig_HSid.append([])
            continue
        HSid = ""
        for company in list_new:
#            print("\n",company)
#            print("\n",contact["identity-profiles"][0]["identities"])
            try:
                HSname = company['properties']['name']['value'] 
#                print("Name is ", HSname)
            except:
                
                continue

            if orig_name == HSname:

                HSid=[company['companyId']]
#                print("HSid is ", HSid)
        if HSid == []:
            orig_HSid.append(["NM + "+orig_name])
        else:
            orig_HSid.append(HSid)
    print("Type being returned: ", type(orig_HSid))
    return orig_HSid

def get_contacts_from_seolist(seolist, contactList):
    contactIDs = []
    print("in get contacts from seo")
    print(seolist)
    for contact in contactList:

        if 'seoname' in contact['properties']:
#            print("Has seoname")

            if contact['properties']['seoname']['value'] in seolist:
#                print('in list')
#                print(contact)
                contactIDs.append(contact['vid'])

    return(contactIDs)


def get_companyID_from_seo(seo, companyList):
    companyIDs = []
    companySeos = []
    companyNames = []
    brandNames = []
    for company in companyList:

        if 'seoname' in company['properties']:
            if company['properties']['seoname']['value'] == seo:
#                print(company['properties'])
                companyIDs.append(company['companyId'])
                companySeos.append(seo)
                if 'name' in company['properties']:
                    companyNames.append(company['properties']['name']['value'])
                else:
                    companyNames.append("")
                if 'brand_name' in company['properties']:
                    brandNames.append(company['properties']['brand_name']['value'])
                else:
                    brandNames.append("")

    return(companyIDs, companySeos, companyNames,brandNames)

def get_companyID_from_name(name, companyList):
    companyIDs = []
    for company in companyList:

        if 'name' in company['properties']:
            if company['properties']['name']['value'] == name:
                companyIDs.append(company['companyId'])
    return(companyIDs)

def match_deals_byname(df_orig, list_new):
    orig_HSid = []
    for i in range(len(df_orig)):
#        print("Person ", df_orig.Name[i])
#        print("Email ", df_orig.Email[i])
        orig_name = df_orig[i]
#        print ("deal name is", orig_name)
        if orig_name == "":
            orig_HSid.append([])
            continue
        HSid = ""
        for deal in list_new:
#            print("\n",deal)
#            print("\n",contact["identity-profiles"][0]["identities"])
            try:
                HSname = deal['properties']['dealname']['value']
 #               print("deal name is ", HSname)
            except:
                orig_HSid.append([])
                continue

            if orig_name == HSname:

                HSid=[deal["dealId"]]
                print("type HSid is ", type(HSid))
        if HSid == []:
            orig_HSid.append(["NM + "+orig_name])
        else:
            orig_HSid.append(HSid)
    print("Deal type being returned: ", type(orig_HSid))
    return orig_HSid

def update_HSowners(bearer, newids, contacts):
    for i in range(len(contacts)):
        try:
            ID = lookup_HSowner(contacts.Owner[i])
        except:
            continue
#        print("\nHsids ", HSids[i])
#        print("PD_Contact ", PD_contacts.Email[i])
#        print("ID ", ID)
        url ='https://api.hubapi.com/contacts/v1/contact/vid/'+str(newids[i])+'/profile'
        headers = {
        'Authorization': 'Bearer '+bearer
        }
        headers['Content-Type']= 'application/json'

        data=json.dumps({ "properties": 
            [{
                "property": "hubspot_owner_id",
                "value": ID
            },
            ]
            
        })

        r = requests.post(data=data, url=url, headers=headers)

#        print(r.status_code)
#        print(r)
    print("Looks good")
    return()



bearer_token = 'pat-eu1-afd33a4b-29ac-4efa-a4bb-41f1d3e37afe'


def create_ids_dict(origin, new):
    #create lookup dictionary from contact ID in old account to contact ID in new account
    ids_dict = {}
    for contact_old in origin:
    #    print("\n\n")
        email_old= get_email(contact_old)
        for contact_new in new:
            email_new = get_email(contact_new)
            if email_old == email_new:
                ids_dict[contact_old['vid']] = contact_new['vid']
    return(ids_dict)

def create_companies_dict(origin_comp, new_comp):
#    TODO: complete this
    #create lookup dictionary from contact ID in old account to contact ID in new account
    companies_dict = {}
    for company_old in origin_comp:
    #    print("\n\n")
        domain_old= get_email(company_old)
        for contact_new in new:
            email_new = get_email(contact_new)
            if email_old == email_new:
                ids_dict[contact_old['vid']] = contact_new['vid']
    return(companies_dict)

def create_deal_dict(origin_comp, new_comp):
#    TODO: complete this
    #create lookup dictionary from contact ID in old account to contact ID in new account
    companies_dict = {}
    for company_old in origin_comp:
    #    print("\n\n")
        domain_old= get_email(company_old)
        for contact_new in new:
            email_new = get_email(contact_new)
            if email_old == email_new:
                ids_dict[contact_old['vid']] = contact_new['vid']
    return(companies_dict)


def get_summary(bearer_token):
    print("getting contacts")
    get_contacts(bearer_token)
    print("getting companies")
    get_companies(bearer_token)
    print("getting deals")
    get_deals(bearer_token)

    print("getting engagements")
    get_engagements(bearer_token)


def HS_create_contact(HS_update):

    update=[]
    for prop in HS_update:
        HS_prop = prop_map[prop]['HS']
        if prop == 'dob':
            HS_update[prop]=int(1000*datetime.strptime(HS_update[prop], "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
        if prop == 'street_address' and HS_update[prop].strip()==",":
            HS_update[prop]=""
        if prop != 'HS_id':
            update.append({"property":HS_prop,"value":HS_update[prop].strip()})
    properties = {"properties":update}
    newHScontact = json.dumps(properties)
    print("Creating HS contact\n", newHScontact)


    url = 'https://api.hubapi.com/contacts/v1/contact/'
    headers = {
    'Authorization': 'Bearer '+HS_token,
    'Content-Type': "application/json"  
    }

    r = requests.post( url = url, data = newHScontact, headers = headers )
    print(r.text)
    return(r.json())

def rerun_badnotes():

    file = open("notes-not-uploaded.obj","rb")
    not_done = pickle.load(file)
    file.close()

    print(len(not_done))

    notes_left = []
    for note in not_done:
        if ((note["companies"]==[] or type(note["companies"][0])==int) and (note["deals"]==[] or type(note["deals"][0])==int)):
            note["body"]=note["body"] + "  (Pipedrive contact not found, name is "+note["contacts"][0][5:]+")"
            note["contacts"] = []
            print("NOTE: ", note["body"])
            upload_note(bearer_token, note)
        else:
            notes_left.append(note)


    print(len(notes_left))
    filehandler = open("notes-not-uploaded2.obj","wb")
    pickle.dump(notes_left, filehandler)
    filehandler.close()

#print("all done")


bearer_from_artesian = 'pat-na1-08f29545-1d80-40e9-adee-93c67b379b5b' #artesian
bearer_from_seaview = 'pat-na1-16523000-177f-49dc-8e13-84fe34277667' #seaview
bearer_to = 'pat-na1-c5b8288f-d782-4402-962c-cfb8ee5b1922' #vidclose


def make_unique(activity):
    if 'bodyPreview' in activity['engagement']:
        engageunique = activity['engagement']['type']+str(activity['engagement']['timestamp'])+activity['engagement']['bodyPreview']+ \
        str(''.join([str(x) for x in activity['associations']['contactIds']]))#+ \
#        str(''.join([str(x) for x in activity['associations']['companyIds']]))+ \
#        str(''.join([str(x) for x in activity['associations']['dealIds']]))
    elif 'sourceID' in activity['engagement']:
        engageunique = activity['engagement']['type']+str(activity['engagement']['timestamp'])+activity['engagement']['sourceId']+ \
        str(''.join([str(x) for x in activity['associations']['contactIds']]))#+ \
#        str(''.join([str(x) for x in activity['associations']['companyIds']]))+ \
#        str(''.join([str(x) for x in activity['associations']['dealIds']]))               
    elif 'subject' in activity['metadata']:
        engageunique = activity['engagement']['type']+str(activity['engagement']['timestamp'])+activity['metadata']['subject']+ \
        str(''.join([str(x) for x in activity['associations']['contactIds']]))#+ \
#        str(''.join([str(x) for x in activity['associations']['companyIds']]))+ \
#        str(''.join([str(x) for x in activity['associations']['dealIds']])) 
    elif 'disposition' in activity['metadata']:
        engageunique = activity['engagement']['type']+str(activity['engagement']['timestamp'])+activity['metadata']['disposition']+ \
        str(''.join([str(x) for x in activity['associations']['contactIds']]))#+ \
#        str(''.join([str(x) for x in activity['associations']['companyIds']]))+ \
#        str(''.join([str(x) for x in activity['associations']['dealIds']])) 
    elif 'title' in activity['metadata']:
        engageunique = activity['engagement']['type']+str(activity['engagement']['timestamp'])+activity['metadata']['title']+ \
        str(''.join([str(x) for x in activity['associations']['contactIds']]))#+ \
#        str(''.join([str(x) for x in activity['associations']['companyIds']]))+ \
#        str(''.join([str(x) for x in activity['associations']['dealIds']])) 
    elif 'body' in activity['metadata']:
        engageunique = activity['engagement']['type']+str(activity['engagement']['timestamp'])+activity['metadata']['body']+ \
        str(''.join([str(x) for x in activity['associations']['contactIds']]))#+ \
#        str(''.join([str(x) for x in activity['associations']['companyIds']]))+ \
#        str(''.join([str(x) for x in activity['associations']['dealIds']])) 
    else:
        print("another -- can't make unique")
        print(activity)
        input()
    return engageunique


def find_dup_engagements(bearer_token):
    activities = get_engagements(bearer_token)
    uniques = []
    for activity in activities:
        engageunique =  make_unique(activity)
        uniques.append(engageunique)

    dup_inds = []
    dup_items=[]
    with open('activities.txt', 'w') as f:
        f.writelines(uniques)

    uniques_set=[]
    print('uniques: ', len(uniques))
    for i, item in enumerate(uniques):
        if item not in uniques_set:
            uniques_set.append(item)
        else:
#            print("duplicate: ", item)
            dup_inds.append(i)
            dup_items.append(item)
    print("number of dups", len(dup_inds))
    print("number of items", len(dup_items))

    for j, item in enumerate(dup_items):
        print("\nj", j, item)
        index=dup_inds[j]
#        print(activities[j])
        print("unique identifier : ", item)

        print("id#1: ", activities[index]['engagement']['id'])
        print(activities[index])

        if len(item)>30:
            delete_engagement(activities[index]['engagement']['id'], bearer_token)
        else:
            ans = input("delete?")
            if ans.lower() == 'y':
                delete_engagement(activities[index]['engagement']['id'], bearer_token)
    return

def get_email_from_ID(emailID):

    url = "https://api.hubapi.com/crm/v3/objects/emails/"+emailID

    querystring = {"properties":["hs_email_text","hs_email_sender_firstname","hs_email_sender_lastname","hs_email_subject","hs_email_to_firstname","hs_email_to_lastname","hs_email_sender_email","hs_email_to_email"],"archived":"false"}
    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + bearer_token
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    r = json.loads(response.text)
    return(r)

def format_email(email):
    """uses return object from get_mail_from_ID"""
    output = ""
    for val in email["results"]:
        output = output + "\n\n\n***************************************************************"
        output = output + "\n\n\nFrom: "
        sender_fn = val["properties"]["hs_email_sender_firstname"]
        sender_ln = val["properties"]["hs_email_sender_lastname"]
        if sender_fn !=None: 
            output = output + " " + sender_fn + " " + sender_ln + " "
        output = output + val["properties"]["hs_email_sender_email"]
        output = output + "\nTo: "
        to_fn = val["properties"]["hs_email_to_firstname"]
        to_ln = val["properties"]["hs_email_to_lastname"]
        if to_fn !=None: 
            output = output + " " + to_fn + " " + to_ln+" "

        output = output + val["properties"]["hs_email_to_email"]
        output = output + "\nSubject: " + val["properties"]["hs_email_subject"]
        output = output + "\n\n" + val["properties"]["hs_email_text"]
    print(output)

#get_summary(bearer_to)
#input()
#look up manually: under properties, contact owner
#owner_dict = {84595049:125818778, 49059542:125818777, 49060147:125821094, 49060156:125821097, 53262124:125821096, 107960726:1, 121556251:1, 49060152:1, 68926553:1, 108344969:1}

#sync_engagements(bearer_from_artesian, bearer_to, owner_dict, do_update=False)

#find_dup_engagements(bearer_to)


#get_summary(bearer_to)
#read_and_upload_activities(activities)



#print("Artesian")
#get_summary(bearer_from_artesian)
#print("Seaview")
#get_summary(bearer_from_seaview)
#print("Vidclose")
#get_summary(bearer_to)

#artesian_contacts = get_contacts(bearer_from_artesian)
#vid_contacts = get_contacts(bearer_to)
#ids_dict = create_ids_dict(artesian_contacts, vid_contacts)
#print(ids_dict)

#copy_contact_owners(bearer_from_artesian, bearer_to, ids_dict)
#read_and_upload_notes()
#read_and_upload_activities()
 
#rerun_badnotes()
def get_contact_property(property, contact_record):
    if property in contact_record['properties']:
        property_value = contact_record['properties'][property]['value'].replace(",", " ")
        return(property_value)
    else:
        return("UNK")
        

def process_seos(seolist):
#    print("in process")
    #HScompanies = get_companies()
    HScontacts = get_contacts()
#    print("got contacts")
    #companylist = pd.read_csv("hubspot_companies.csv", names=["name", "seo", "c1", "c2", "c3", "note"])
    #seolist = pd.read_csv("seo exports - Sober October.csv")
    #seolist = pd.read_csv("seo exports - Autumn.csv")
#    listname = "seo exports - Halloweekender"
#    listname = "seo exports - Autumn"
    #listname = "seo exports - Sober October"
    #seolist = pd.read_csv(listname + ".csv")
#    print(seolist)

#    output_file = "First Name" + ","+ "Job Title"+ ","+"BrandName"+ ","+"Company"+","+"Seoname"+","+"Email"+"\n"
    seos = seolist

    print(len(seos), len(HScontacts))
    contactIDs = get_contacts_from_seolist(seos, HScontacts)
    numcontacts = len(contactIDs)
    st.write("Processing ", numcontacts, " contacts")
    fname = []
    fname2 = []
    lname = []
    email=[]
    jobtitle=[]
    jobroletype=[]
    brandname=[]
    company=[]
    seo=[]
    count=1
    for contactID in contactIDs:
        if len(fname)>count * numcontacts/10:
            st.write(count*10, " percent done")
            count+=1
        contact_record = get_contact_byID(str(contactID))

        fname.append(get_contact_property('firstname', contact_record))
        lname.append(get_contact_property('lastname', contact_record))
        email.append(get_contact_property('email', contact_record))
        brandname.append(get_contact_property('brand_name', contact_record))
        company.append(get_contact_property('company', contact_record))
        jobroletype.append(get_contact_property('job_role_type__don_t_change_', contact_record))
        jobtitle.append(get_contact_property('jobtitle', contact_record))


        seo.append(contact_record['properties']['seoname']['value'])

    output = {"First name":fname, "Last name":lname, "Job title":jobtitle, "Job role type":jobroletype, "Brand name":brandname, "Company":company, "seoName":seo, "Email":email}
    output_file = pd.DataFrame(output)#list(zip(fname, jobtitle, brandname, company, seo, email)))
    return(output_file)

    #output = pd.DateFrame
    #    print("\n")
    #    print(contact_fname)# + ' ' + contact_lname)
    #    print(contact_email)
    #    print(contact_jobtitle)


st.title("Get contacts for SEO list")


#st.write("Upload your bad URL file here")
seolist = st.file_uploader("Upload your SEO list")
if seolist is not None:
    seolist = pd.read_csv(seolist)

    try:
        seolist = seolist['seoName']
    except:
        st.write("Your file must have a column with the heading 'seoName'")


    #finally, turn it into a list of strings

    seolist = list(seolist)
#    print("now a list")
#    seolist = seolist.getvalue().decode('UTF-8')
    print(seolist)
    time_to_process = st.button("Ready to process")
    if time_to_process:
#        try:
        output_file = process_seos(seolist)
        print(output_file['seoName'])
        noContactsFound = list(set(seolist) - set(output_file['seoName']))
        print(noContactsFound)
        st.write("No contacts found for these seoNames: ", noContactsFound)
        # except Exception as e:
        #     st.write("Error\n", e)
        #     output_file=[]

        if len(output_file)>0:
            @st.cache
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')

            csv = convert_df(output_file)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='email_list.csv',
                mime='text/csv',
            )