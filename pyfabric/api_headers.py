import requests

class FabricClient:
    """Cliente para autenticação e requisições ao Microsoft Fabric/Power BI."""
    
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.access_token = None
    
    def get_access_token(self):
        """Busca o token de acesso do requisitante."""
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        scope = "https://analysis.windows.net/powerbi/api/.default"
        
        token_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope
        }
        
        try:
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            
            response_data = token_response.json()
            
            if 'access_token' not in response_data:
                raise ValueError(f"No access token in response: {response_data}")
            
            self.access_token = response_data['access_token']
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")
    
    @property
    def headers(self):
        """Retorna os headers com token de autenticação."""
        if not self.access_token:
            self.get_access_token()
        
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }