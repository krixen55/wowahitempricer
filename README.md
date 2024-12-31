# wowahitempricer
Finds cheapest auction items across all AHs region-wide

# How to use

## Create secrets.json file (blank one provided)

Check out section "Client ID and secret" at the following link:

https://develop.battle.net/documentation/guides/using-oauth

excerpt:

The first step in using OAuth is getting a client_id and client_secret via the API Access tool:

Log in to the Developer Portal.
Click Create New Client.
Enter a client name. The client name is used to identify the client in the list view. Client names may be visible to your site users and globally unique across all developer accounts.

Enter any redirect URIs needed (see below for details). Note: the Developer Portal does not validate redirect URIs entered by developers.

Enter the URL for the client application your are building and a description of your intended use for the APIs.

Once you have the client id and secret, input them into the "secrets.json" file.

## Running the code

I didn't create any CLI for this, open up the ah_pricer.py file and at the top, change 

ITEM_ID - to the item you are trying to price, use wowhead to find item id

REGION - to the region you are using 

then run 

```
python ah_pricer.py
```

by default, it prints the 3 cheapest options... however, you can play with the sorted data in the main function anyway you want. use GPT if you are not used to coding

Thanks for checking this out, if there is a lot of intrest, i can improve on this in the future
