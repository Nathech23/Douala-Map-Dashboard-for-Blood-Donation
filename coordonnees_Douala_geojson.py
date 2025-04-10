#import pandas as pd

#df = pd.read_csv(r'C:\Users\DELL E5580\Documents\IndabaX-2025\donneurs_oui.csv', sep=';', encoding='utf-8-sig')
#df_trie = df.sort_values(by='Quartier de Résidence')  
#df_trie.to_csv('donnees_tries.csv', index=False, sep=';', encoding='utf-8-sig')

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import json
import os

# Initialiser le géocodeur avec un user-agent plus descriptif
geolocator = Nominatim(user_agent="douala_neighborhoods_geocoder")

# Liste des quartiers de Douala
quartiers = [
    "village", "yassa", "deido", "logbaba", "bonaberi", "nyalla", "bonamoussadi",
    "ndogpassi", "new bell", "makepe", "newbell", "bali", "pk8", "pk12", "ngodi bakoko",
    "pk9", "bependa", "bepanda", "kotto", "pk14", "pk11", "boko", "bonapriso", "logpom",
    "akwa", "dakar", "oyack", "pk10", "beedi", "ndogbong", "ndogpassi 2", "cité des palmiers",
    "japoma", "nkongmondo", "nyalla pariso", "r a s", "bilongue", "new-bell", "bonaberie",
    "edea", "logbessou", "ndogpassi 3", "pas précisé", "non precisé", "pas precise",
    "ndongbong", "non précisé", "mboko", "ndokoti", "bessengue", "cite des palmiers",
    "bonaloka", "cité sic", "pk 10", "sic cacao", "pk16", "ras", "youpwe", "nboko",
    "pk15", "ngodi", "newton aéroport", "nkomondo", "pas precisé", "yatika", "déido",
    "pk13", "total nkolobong", "tradex borne 10", "bependa omnisport", "cite cicam",
    "cité de palmiers", "carrefour agip", "brazzaville", "cite sic", "ngodi akwa",
    "ndopassi", "ndokotti", "logbaba jardin", "japouma", "madagascar", "parisot nyalla",
    "bonateki deido", "brazaville", "bp cité", "ange raphael", "akwa nord", "akwa-nord",
    "bastos", "ange rafael", "ange raphaël", "bafoussam", "bonendale", "bonapriso rue koloko",
    "bependa maturite", "bona priso goupwe", "bonamodoro diedo", "hôpital général",
    "godi bokocie", "genie militaire", "entrée mini cité cogefar", "elf (rond point)",
    "enri", "douala(non) précisé", "douala-douala", "douala 812.12", "dibombari",
    "douala oyack", "douala ndopassiz", "deïdo", "douala ccc", "cité-sic", "cité-sic bassa",
    "carrefour ari", "cite de la paix", "cité cicam", "carrefour bonabassem", "cite cic",
    "cité cic", "cité belge", "bonambappe", "bp cite", "borne 10 village", "bonateki",
    "bonanjo", "bonamikano", "bwang bakoko", "cite de bille", "congefar", "binamoussadi",
    "billongue", "besengue", "bependa tonnerre", "bependa aeroport", "bependa casmando",
    "boko plage", "bois des singes", "bonabéri", "bonamousadi", "bomono ba mbengue",
    "bonaberi sctm", "bonadibong", "bonabéri (grand baobab)", "bonadoumbe", "bepanda omnisport",
    "bonaorisso", "ari", "aucun", "anhe rafael", "ange raphael campus 2", "ancien abatoire",
    "mbangopongo", "ndobassi 2", "ndog passi 3", "ndog-passi", "mboppi", "logbaba st thomad",
    "kotto- chefferie", "kms", "jardin ndogmbe", "hôpital général de douala", "new-deido",
    "new-bell /nkouloulou", "new ton aeroport", "ndokotti ccc", "ndogpassi iii", "ndogbon",
    "ndogpassi i", "ndogpassi ii", "nyalla chateau", "non precise", "ndg-bong",
    "ndogpassi village", "nialla", "nkong-mondo", "nkonguondo", "nkonmondo", "ndogpassi 1",
    "logbaba saint thomas", "logbaba plateau", "log baba", "log-baba", "kambo boko",
    "mballa 2", "missole ii", "manjo", "makepe missoke",  "mbanga", "pk13 bassa", "nyala", "nkol mbong", "ngodi- bakoko", "pk12 mandjab", "pk 13", "pk 11", "pk21", "pihidibamba", "nylon", "nyalla pariazo", "nkolbong", "ngodi- akwa", "soubom", "pl12", "pk5", "rond point ccc", "rue koloko bonapriso", "song mahop", "tombel", "texaco aéroport", "total nkolbong",
    "village marché", "tradex village", "yaounde", "yaoundé" , "yatchika", "yassa tika", "bonakouamouang", "nyala château"

]

# Fonction pour géocoder avec gestion des erreurs et retry
def geocode_with_retry(quartier, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            query = f"{quartier}, Douala, Cameroun"
            result = geolocator.geocode(query, timeout=10)
            return result
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt == max_retries - 1:
                print(f"Échec après {max_retries} tentatives pour {quartier}: {e}")
                return None
            print(f"Tentative {attempt+1} échouée pour {quartier}, nouvel essai dans {delay}s...")
            time.sleep(delay)
    return None

# Préparer la structure de données GeoJSON
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

# Nom du fichier de sortie
output_file = "quartiers_douala.geojson"

# Traiter chaque quartier
for i, quartier in enumerate(quartiers):
    print(f"Traitement de {quartier} ({i+1}/{len(quartiers)})...")
    
    location = geocode_with_retry(quartier)
    
    if location:
        # Créer un Feature GeoJSON pour ce quartier
        feature = {
            "type": "Feature",
            "properties": {
                "nom": quartier,
                "adresse": location.address
            },
            "geometry": {
                "type": "Point",
                "coordinates": [location.longitude, location.latitude]
            }
        }
        
        geojson_data["features"].append(feature)
        print(f"{quartier}: [{location.longitude}], [{location.latitude}]")
        
        # Sauvegarder périodiquement (par exemple tous les 10 quartiers)
        if (i + 1) % 10 == 0 or i == len(quartiers) - 1:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(geojson_data, f, ensure_ascii=False, indent=2)
            print(f"Sauvegarde intermédiaire effectuée ({i+1} quartiers traités)")
    else:
        print(f"{quartier}: Non trouvé")
    
    # Pause entre les requêtes pour respecter les limites du service
    time.sleep(1.5)

# Sauvegarde finale
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print(f"Terminé! Les résultats ont été sauvegardés dans {output_file}")