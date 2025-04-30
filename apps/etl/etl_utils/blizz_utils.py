import json, time, requests
from config import CACHE_FILE, CLIENT_ID, CLIENT_SECRET, BLIZZ_API, NAMESPACE, LOCALE, BLIZZ_TOKEN_URL

class BlizzUtils:
    def __init__(self):
        self.token = self.get_access_token()

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
        url   = BLIZZ_API + path
        headers = {"Authorization": f"Bearer {self.token}"}
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
    
    def get_specs_dict(self) -> dict:
        """
        Returns a dictionary with the name of the specialization as the key and the id and href as the values.
        """
        print("[ETL] Getting specs...")
        response = self.api_get("/data/wow/playable-specialization/index")

        spec_dict = {}
        for v in response["character_specializations"]:
            spec_dict[v["name"]] = {
                'href': v['key']['href'], 'id': v['id'],
                "spec_nodes": [], "hero_talent_nodes": []
            }

        return spec_dict
    
    def merge_specs_into_classes_dict(self, classes_dict: dict, specs_dict: dict) -> dict:
        """
        Merges the specs into the classes dictionary.
        """
        print("[ETL] Merging specs into classes...")
        
        for _, spec_data in specs_dict.items():
            specId = spec_data["id"]
            response = self.api_get(f"/data/wow/playable-specialization/{specId}")
            
            original_class = response["playable_class"]["name"]
            spec_data["spec_name"] = response["name"]

            classes_dict[original_class]["specs"].append(spec_data)

        return classes_dict
    
    def get_talent_trees_urls(self):
        """
        Returns a dictionary with the name of the talent tree as the key and the url as the value.
        """

        print("[ETL] Getting talent trees urls...")
        response = self.api_get(f"/data/wow/talent-tree/index")

        spec_talent_trees = {}
        for item in response["spec_talent_trees"]:
            spec_talent_trees[item["name"]] = item["key"]["href"].split("?namespace")[0].split(".com")[1]

        class_talent_trees = {}
        for item in response["class_talent_trees"]:
            class_talent_trees[item["name"]] = item["key"]["href"].split("?namespace")[0].split(".com")[1]

        hero_talent_trees = {}
        for item in response["hero_talent_trees"]:
            hero_talent_trees[item["name"]] = item["key"]["href"].split("?namespace")[0].split(".com")[1]

        return spec_talent_trees, class_talent_trees, hero_talent_trees
    
    def extract_class_skills_info(self, class_dict, class_talent_trees):
        for class_name in class_dict:
            response = self.api_get(class_talent_trees[class_name])

            for node in response["talent_nodes"]:
                try:
                    # Check if node has choice_of_tooltips
                    if "choice_of_tooltips" in node["ranks"][0]:
                        # Process choice nodes
                        for choice in node["ranks"][0]["choice_of_tooltips"]:
                            spell_name = choice["talent"]["name"]
                            spell_description = choice["spell_tooltip"]["description"]
                            class_dict[class_name]["class_nodes"].append((spell_name, spell_description))
                    else:
                        # Process regular nodes (original code)
                        spell_name = node["ranks"][0]["tooltip"]["spell_tooltip"]["spell"]["name"]
                        spell_description = node["ranks"][0]["tooltip"]["spell_tooltip"]["description"]
                        class_dict[class_name]["class_nodes"].append((spell_name, spell_description))
                except:
                    print("Skipping node: ", node)
            print(class_dict[class_name]["class_nodes"])

        return class_dict
    
    @staticmethod
    def process_talent_node(node, target_list):
        """Process a single talent node and add it to the target list."""
        try:
            if "choice_of_tooltips" in node["ranks"][0]:
                # Process choice nodes
                for choice in node["ranks"][0]["choice_of_tooltips"]:
                    spell_name = choice["talent"]["name"]
                    spell_description = choice["spell_tooltip"]["description"]
                    target_list.append((spell_name, spell_description))
            else:
                # Process regular nodes
                spell_name = node["ranks"][0]["tooltip"]["spell_tooltip"]["spell"]["name"]
                spell_description = node["ranks"][0]["tooltip"]["spell_tooltip"]["description"]
                target_list.append((spell_name, spell_description))
            return True
        except:
            return False
    
    def process_hero_talent_trees(self, hero_trees, target_list):
        """Process all hero talent trees and add nodes to the target list."""
        for tree in hero_trees:
            for node in tree["hero_talent_nodes"]:
                if not self.process_talent_node(node, target_list):
                    print("Skipping node: ", node)

    def extract_spec_talents(self, class_dict, spec_talent_trees):
        """Extract all talent information for each class and specialization."""
        for class_name in class_dict:
            print("Exploring class: ", class_name)
            for spec in class_dict[class_name]["specs"]:
                print("Exploring spec: ", spec["spec_name"])
                print(spec_talent_trees[spec["spec_name"]])
                response = self.api_get(spec_talent_trees[spec["spec_name"]])
                
                # Process spec talent nodes
                for item in response["spec_talent_nodes"]:
                    if not self.process_talent_node(item, spec["spec_nodes"]):
                        print("Skipping node: ", item)
                
                # Process hero talent nodes
                self.process_hero_talent_trees(response["hero_talent_trees"], spec["hero_talent_nodes"])
        
        return class_dict