import json, time, requests
from config import CACHE_FILE, CLIENT_ID, CLIENT_SECRET, BLIZZ_API, NAMESPACE, LOCALE, BLIZZ_TOKEN_URL

class BlizzUtils:
    def __init__(self):
        self.token = self.get_token()

    @staticmethod
    def get_access_token() -> str:
        if CACHE_FILE.exists():
            data = json.loads(CACHE_FILE.read_text())
            if time.time() < data["expires_at"] - 60:
                return data["access_token"]

        if not CLIENT_ID or not CLIENT_SECRET:
            raise RuntimeError("Defina BLIZZ_CLIENT_ID e BLIZZ_CLIENT_SECRET")

        resp = requests.post(
            BLIZZ_TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=(CLIENT_ID, CLIENT_SECRET),
            timeout=20
        )
        resp.raise_for_status()
        data = resp.json()
        data["expires_at"] = time.time() + data["expires_in"]
        CACHE_FILE.write_text(json.dumps(data))
        return data["access_token"]

    def api_get(self, path: str) -> dict:
        token = self.get_access_token()
        url   = BLIZZ_API + path
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(
            url,
            params={"namespace": NAMESPACE, "locale": LOCALE},
            headers=headers,
            timeout=20
        )
        resp.raise_for_status()
        return resp.json()    
    def get_classes_dict(self) -> dict:
        """
        Returns a dictionary with the name of the class as the key and the id and href as the values.
        """
        print("[ETL] Getting classes...")
        response = self.api_get("/data/wow/playable-class/index")
        
        class_dict = {}
        for v in response["classes"]:
            class_dict[v["name"]] = {
                'href': v['key']['href'], 'id': v['id'], 
                "specs": [], "class_nodes": []
            }

        return class_dict
    