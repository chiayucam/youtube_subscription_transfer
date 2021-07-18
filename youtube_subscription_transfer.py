import os
import sys
import json
import time
import argparse
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from distutils.util import strtobool

def get_arguments():
    parser = argparse.ArgumentParser(prog="Youtube subscription transfer", description="This program supports subscription exportation and importation from any youtube account")
    parser.add_argument("command", nargs=1, type=command_type, help="use commands:\nexport\nimport")
    parser.add_argument("filename", nargs=1, type=str, help="Subsription json filename to export or import")
    args = parser.parse_args()
    return args

def command_type(string):
    if not (string=="export" or string=="import"):
        raise argparse.ArgumentTypeError("Invalid command")
    return string

def check_dir(required_dirs):
    for required_dir in required_dirs:
        if not os.path.isdir(required_dir):
            os.mkdir(required_dir)
        
def check_client_secrets_file_exist(client_secrets_file):
    if not os.path.isfile(client_secrets_file): 
        sys.exit("client_id.json not found")

def create_API_client(scopes, api_service_name, api_version, client_secrets_file):
    check_client_secrets_file_exist(client_secrets_file)
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

def export_subscriptions(youtube):
    pageToken = ""
    subscriptions = []

    while True:
        request = youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=50,
            order="alphabetical",
            pageToken=pageToken
        )
        response = request.execute()
        subscriptions = [*subscriptions, *retrive_page_data(response['items'])]

        if 'nextPageToken' not in response:
            break
        pageToken = response['nextPageToken']

    print("total subscriptions retrived: {}".format(response['pageInfo']['totalResults']))
    return subscriptions

def retrive_page_data(items):
    page_data = []
    for item in items:
        page_data.append({"title": item['snippet']['title'],
                         "ID": item['snippet']['resourceId']['channelId']})
    return page_data

def remove_matching_subscriptions(source_subscriptions, target_subscriptions):
    for source_subscription in source_subscriptions:
        for target_subscription in target_subscriptions:
            if source_subscription['ID'] == target_subscription['ID']:
                print("{0:<50} subscription already exist, removing from import list")
                source_subscriptions.remove(source_subscription)
                target_subscriptions.remove(target_subscription)
    return source_subscriptions

def import_subscriptions(youtube, subscriptions):
    for subscription in subscriptions:
        request = youtube.subscriptions().insert(
                part="snippet",
                body={
                  "snippet": {
                    "resourceId": {
                      "kind": "youtube#channel",
                      "channelId": subscription['ID']
                    }
                  }
                }
            )
        response = request.execute()
        print("successfully subscribed to {0:>50}".format(subscription['title']))
    print("subscription importing complete")

def read_json(filename):
    read_path = "./json/"+filename
    try:
        with open(read_path, 'r') as f:
            subscriptions = json.load(f)
        return subscriptions
    except (IOError, FileNotFoundError) as e:
        print("file {} does not exist in json directory".format(filename))
        
def save_json(subscriptions):
    save_path = "./json/"+args.filename[0]
    with open(save_path, "w") as f:
        json.dump(subscriptions, f)
        print("saved subscriptions as {} in json directory".format(filename))

        

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    required_dirs = ["./client_secrets_file", "./json"]
    check_dir(required_dirs)
    args = get_arguments()
    if args.command[0]=="export":
        # authorize source account
        print("authorize the Youtube account you wish to transfer subscriptions from")
        youtube = create_API_client(scopes=["https://www.googleapis.com/auth/youtube.readonly"],
                                   api_service_name="youtube",
                                   api_version="v3",
                                   client_secrets_file="./client_secrets_file/client_id.json")
        # retrive source subscriptions
        source_subscriptions = export_subscriptions(youtube) 
        save_json(source_subscriptions)
    elif args.command[0]=="import":
        source_subscriptions = read_json(args.filename[0])
        # authorize target account
        print("authorize the Youtube account you wish to transfer subscriptions to")
        youtube = create_API_client(scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
                                   api_service_name="youtube",
                                   api_version="v3",
                                   client_secrets_file="./client_secrets_file/client_id.json")
        # retrive target subscriptions
        target_subscriptions = export_subscriptions(youtube)
        subscriptions = remove_matching_subscriptions(source_subscriptions, target_subscriptions)
        import_subscriptions(youtube, subscriptions)
    else:
        sys.exit("exiting program")

if __name__ == "__main__":
    main()
