from flask import current_app as app
import msal

class AadService:
    def get_access_token():
        response = None
        try:
            if app.config['AUTHENTICATION_MODE'].lower() == 'masteruser':

                # Create a public client to authorize the app with the AAD app
                clientapp = msal.PublicClientApplication(app.config['CLIENT_ID'], authority=app.config['AUTHORITY'])
                accounts = clientapp.get_accounts(username=app.config['POWER_BI_USER'])

                if accounts:
                    # Retrieve Access token from user cache if available
                    response = clientapp.acquire_token_silent(app.config['SCOPE'], account=accounts[0])

                if not response:
                    # Make a client call if Access token is not available in cache
                    response = clientapp.acquire_token_by_username_password(app.config['POWER_BI_USER'], app.config['POWER_BI_PASS'], scopes=app.config['SCOPE'])     

            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            elif app.config['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
                authority = app.config['AUTHORITY'].replace('organizations', app.config['TENANT_ID'])
                clientapp = msal.ConfidentialClientApplication(app.config['CLIENT_ID'], client_credential=app.config['CLIENT_SECRET'], authority=authority)

                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=app.config['SCOPE'])

            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))