import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_service, save_ga_report, check_ga_report_exists, update_ga_report

# Define the auth scopes to request.
scope = 'https://www.googleapis.com/auth/analytics.readonly'
key_file_location = 'client_secrets.json'


def get_first_profile_id(service):
    """
    Use the Analytics service object to get the first profile id.

    :param service:
    :return:
    """
    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(accountId=account, webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return


def get_results(service, profile_id, dimensions, metrics, start_date):
    """
    Use the Analytics Service Object to query the Core Reporting API
    for the number of sessions within the past seven days.
    """
    return service.data().ga().get(ids='ga:{}'.format(profile_id),
                                   start_date=start_date,
                                   end_date='today',
                                   metrics=metrics,
                                   dimensions=dimensions).execute()


def save_results(results, start_date):
    # iterate through rows
    for r in results.get('rows', {}):
        title = r[0]
        path = r[1]
        avg_top = r[2]
        top = r[3]
        users = r[4]
        adsense_clicks = r[5]
        adsense_revenue = r[6]

        if not check_ga_report_exists(path):
            save_ga_report(title, path, avg_top, top, start_date, users, adsense_clicks, adsense_revenue)
        else:
            update_ga_report(avg_top, top, path, users, adsense_clicks, adsense_revenue)


# Authenticate and construct service.
service = get_service(api_name='analytics',
                      api_version='v3',
                      scopes=[scope],
                      key_file_location=key_file_location)

profile_id = get_first_profile_id(service)

start_date = '90daysAgo'
r = get_results(service, profile_id,
                'ga:pageTitle, ga:PagePath',
                'ga:avgTimeOnPage, ga:timeOnPage, ga:users, ga:adsenseAdsClicks, ga:adsenseRevenue',
                start_date)

save_results(r, start_date)
