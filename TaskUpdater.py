import requests

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
    ids = get_done_item_ids()
    if len(ids) != 0:
        print(f"[I] found {len(ids)} elements to be removed.")
        delete_found_items(ids)
    else:
        print("[E] No items to be deleted where found.\n[E] Not invoking deletion function and exiting program.\n[I] if the result is not accurate, make sure everything is set up per the notion api guidelines (https://developers.notion.com/docs)")

if __name__ == '__main__':
    main()