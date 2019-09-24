def get_all_access_view(googleanalytics, only_account=False):
    analytics = googleanalytics.googleauthentication.get_account("analytics", version="v3")
    accounts = analytics.management().accounts().list().execute()
    all_view = []
    if only_account:
        return [{
            "account_id": a['id'],
            "account_name": a["name"]
        }
            for a in accounts['items']
        ]
    for a in accounts['items']:
        account_name = a['name']
        account_id = a['id']
        properties = analytics.management().webproperties().list(accountId=account_id).execute()
        for p in properties['items']:
            property_id = p['id']
            property_name = p['name']
            views = analytics.management().profiles().list(
                accountId=account_id,
                webPropertyId=property_id).execute()
            for v in views['items']:
                view_id = v['id']
                view_name = v['name']
                all_view.append(
                    {'account_name': account_name,
                     'account_id': account_id,
                     'property_name': property_name,
                     'property_id': property_id,
                     'view_id': view_id,
                     'view_name': view_name
                     })
    return all_view
