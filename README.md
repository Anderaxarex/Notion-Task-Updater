# How To Get The Database ID
=================
You should open the python file and replace "DATABASE_ID" with the id of the Task List page that is generated autmatically when you get a Notion account.
to get the database id of the page you want to access the browser version and navigate to the page. the url will look something like this:
===================
https://www.notion.so/XXX?v=ZZZ
===================
XXX is the databse id. It should be 32 characters long, however if anything doesn't match you can consult the notion api documentation at [https://developers.notion.com/docs]


# How To Schedule The Execution
===================
You can either use a service like Heroku and change the script like so:

```python
import requests
import time 

def get_done_item_ids():
    ids = []
    url = "https://api.notion.com/v1/databases/DATABASE_ID/query"

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "authorization": "Bearer INTEGRATION_TOKEN"    
    }

    query = {
       "filter": {
            "property": "Completion",
            "status":{
                "equals":"Done"
            }
       } 
    }

    response = requests.post(url, json=query, headers=headers)

    data = response.json()
    for i in range(len(data["results"])):
        ids.append(data["results"][i]["id"])
    return ids

def delete_found_items(ids):
    if ids is not None:
        for id in ids:
            url = "https://api.notion.com/v1/blocks/{}".format(id)
            headers = {
                "accept": "application/json",
                "Notion-Version": "2022-06-28",
                "authorization": "Bearer INTEGRATION_TOKEN"             
            }
            r = requests.delete(url, headers=headers)
            if r.status_code == 200:
                print(f"[**] {id} deletion request returned a {r.status_code}. Deletion successfull.")

def main():
    while True:
        ids = get_done_item_ids()
        if len(ids) != 0:
            print(f"[I] found {len(ids)} elements to be removed.")
            delete_found_items(ids)
        else:
            print("[E] No items to be deleted where found.\n[E] Not invoking deletion function and exiting program.\n[I] if the result is not accurate, make sure everything is set up per the notion api guidelines (https://developers.notion.com/docs)")
        time.sleep(604800)

if __name__ == '__main__':
    main()
```
or you can use the windows task scheduler and have a task repeated every week, for a tutorial on the windows task scheduler go to [https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page]


# How To Run Script
===================
while I will not insult your intelligence by telling you how to run a python script, I have included a .bat file (for windows) and a .sh file (for Linux) to get the required libraries. It's only requests so most people should have it already installed, but just in case you can get it that way. 