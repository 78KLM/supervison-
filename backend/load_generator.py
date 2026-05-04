import requests
import random
import time

class TrafficGenerator:
    """
    Classe simulant des serveurs qui envoient leur télémétrie.
    """
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.servers = ["SRV-RADAR-01", "SRV-DATABASE-02", "SRV-FRONT-03", "SRV-AUTH-04"]

    def generate_fake_alert(self) -> dict:
        """Génère un dictionnaire contenant de fausses données de serveur."""
        # Génère un faux pourcentage CPU entre 10 et 99.9
        cpu = round(random.uniform(10.0, 99.9), 1)
        
        # Détermine l'état critique en fonction du CPU
        if cpu > 90:
            status = "CRITICAL"
        elif cpu > 75:
            status = "WARNING"
        else:
            status = "OK"

        payload = {
            "server_name": random.choice(self.servers),
            "cpu_usage": cpu,
            "status": status
            # On n'envoie pas le timestamp, FastAPI va le générer seul 
        }
        return payload

    def start_simulation(self, num_requests: int = 5, delay_seconds: float = 1.0):
        """Lance la boucle d'envoi de requêtes HTTP."""
        print(f"🚀 Démarrage de la simulation vers {self.target_url}...")
        
        for i in range(num_requests):
            payload = self.generate_fake_alert()
            
            try:
                # C'est ici que la magie opère : on envoie le dictionnaire en format JSON
                response = requests.post(self.target_url, json=payload)
                
                if response.status_code == 201:
                    print(f"[SUCCÈS] Données envoyées : {payload['server_name']} | CPU: {payload['cpu_usage']}% | Statut: {payload['status']}")
                else:
                    print(f"[ERREUR] L'API a refusé la donnée. Code: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("❌ [FATAL] Impossible de se connecter. Ton API FastAPI est-elle allumée ?")
                break # On arrête la boucle si le serveur est éteint
            
            # On fait une petite pause avant le prochain envoi
            time.sleep(delay_seconds)
            
        print("🏁 Simulation terminée.")

# Point d'entrée du script
if __name__ == "__main__":
    API_ENDPOINT = "http://127.0.0.1:8000/api/alerts"
    
    # On instancie notre objet et on lance 10 requêtes avec 1 seconde d'intervalle
    generator = TrafficGenerator(target_url=API_ENDPOINT)
    generator.start_simulation(num_requests=10, delay_seconds=1.0)