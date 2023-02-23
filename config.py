class BaseConfig(object):
    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'ServicePrincipal'

    # Workspace Id in which the report is present 
    WORKSPACE_ID = ''
    
    # Report Id for which Embed token needs to be generated 
    REPORT_ID = '' 
    
    # IDs of the Azure
    TENANT_ID = ''
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    
    # Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal. 
    SCOPE = ['https://analysis.windows.net/powerbi/api/.default']
    
    # URL used for initiating authorization request 
    AUTHORITY = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode. 
    # POWER_BI_USER = 'gustavo.dias@coloradoagro.com.br'
    
    # Master user email password. Required only for MasterUser authentication mode. 
    # POWER_BI_PASS = 'NoOaJ&ODEsz%'