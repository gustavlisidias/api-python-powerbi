class BaseConfig(object):
    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'ServicePrincipal'

    # Workspace Id in which the report is present 
    WORKSPACE_ID = '55517cfe-0878-456d-ab5f-154674a2625f'
    
    # Report Id for which Embed token needs to be generated 
    REPORT_ID = '0f36ab34-80d8-48a8-8222-f65e40d323f7' 
    
    # IDs of the Azure
    TENANT_ID = '5172280b-54ac-44c1-949a-893f3ee9542f'
    CLIENT_ID = '24f20447-28d6-4dff-8dff-ed8dd1deb4da'
    CLIENT_SECRET = 'mOJ8Q~p~vEtbtB2IDxYhyekXbQMz6q_~gT4eMcWC'
    
    # Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal. 
    SCOPE = ['https://analysis.windows.net/powerbi/api/.default']
    
    # URL used for initiating authorization request 
    AUTHORITY = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode. 
    # POWER_BI_USER = 'gustavo.dias@coloradoagro.com.br'
    
    # Master user email password. Required only for MasterUser authentication mode. 
    # POWER_BI_PASS = 'NoOaJ&ODEsz%'