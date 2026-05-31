import unittest
from fastapi.testclient import TestClient
from src.api.middleware import app

client = TestClient(app)

class TestAdvancedCorporateScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Testler başlamadan önce API'nin ayakta ve kuralların yüklü olduğundan emin ol."""
        with TestClient(app) as c:
            response = c.get("/api/v1/health")
            cls.health_data = response.json()

    def test_project_asset_mismatch_hallucination(self):
        """
        Zorlu Test 1: Çapraz Proje Kirliliği (Cross-Project Contamination)
        Senaryo: LLM, "Dedektif: Satır Arası" oyunu için bir tanıtım metni yazarken,
        yanlışlıkla "İksir Çiçeği" projesinin görsel assetlerini veya altyazılarını dahil ediyor.
        Beklenti: Sistemin CORP_APP_ASSET_MISMATCH kuralını devreye sokup engellemesi.
        """
        payload = {
            "user_prompt": "Dedektif: Satır Arası için yeni bir mağaza açıklaması yaz.",
            "llm_response": {
                "raw_text": "Dedektif: Satır Arası ile gizemleri çözün! (Görsel: iksir_cicegi_bg_01.png kullanıldı)",
                "extracted_facts": {
                    "is_harmful": False,
                    "mixes_project_assets": True  # LLM bu hatayı yaptığını meta veride belli ediyor
                }
            }
        }
        
        response = client.post("/api/v1/process", json=payload)
        data = response.json()
        
        self.assertFalse(data["is_approved"])
        self.assertTrue(any("CORP_APP_ASSET_MISMATCH" in v for v in data["violations"]))

    def test_client_communication_tone_and_budget_leak(self):
        """
        Zorlu Test 2: Müşteri İletişiminde Ton ve Gizlilik İhlali
        Senaryo: Kullanıcı Fatma Hanım veya Mert Bey için bir e-posta taslağı istiyor. 
        LLM hem bütçe müzakerelerini sızdırıyor hem de fazla agresif/iddialı bir ton kullanıyor.
        Beklenti: Z3 motorunun ÇOKLU ihlali (Gizlilik + Ton) aynı anda yakalaması.
        """
        payload = {
            "user_prompt": "Fatma Hanım'a projenin gecikeceğini bildiren bir mail yaz.",
            "llm_response": {
                "raw_text": "Fatma Hanım, projeyi geciktiriyoruz çünkü bütçede anlaştığımız 50.000 TL yetersiz. Şartlarımızı kabul etmezseniz işi bırakırız.",
                "extracted_facts": {
                    "leaks_client_negotiations": True, # Bütçe sızdırıldı
                    "uses_assertive_tone": True        # Ton çok agresif/iddialı, mütevazı değil
                }
            }
        }
        
        response = client.post("/api/v1/process", json=payload)
        data = response.json()
        
        self.assertFalse(data["is_approved"])
        self.assertEqual(len(data["violations"]), 2, "Sistem her iki kurumsal kural ihlalini de bulmalı.")
        self.assertTrue(any("CORP_CLIENT_CONFIDENTIALITY" in v for v in data["violations"]))
        self.assertTrue(any("CORP_TONE_MODESTY" in v for v in data["violations"]))

    def test_dark_matter_secrecy_and_code_truncation(self):
        """
        Zorlu Test 3: Çekirdek IP Sızıntısı ve Kod Kırpma (Truncation)
        Senaryo: Kullanıcı "Dark Matter" projesinden bir bellek havuzu kodu istiyor.
        LLM MTD (Gölge Bellek Taşıma) mantığını ifşa ediyor VE kodu üşenip yarım bırakıyor (...).
        Beklenti: Sistem hem IP sızıntısını hem de eksik kod paylaşımını bloklamalı.
        """
        payload = {
            "user_prompt": "Dark Matter projesinin MTD (Moving Target Defense) kodlarını özetle.",
            "llm_response": {
                "raw_text": "def shadow_memory_move(): \n # Gölge bellek taşıma mantığı burada...\n # Geri kalan 405 satır atlandı.",
                "extracted_facts": {
                    "leaks_dark_matter_logic": True, # IP Sızıntısı
                    "truncates_code": True           # Kod eksik bırakıldı (bütünlük bozuldu)
                }
            }
        }
        
        response = client.post("/api/v1/process", json=payload)
        data = response.json()
        
        self.assertFalse(data["is_approved"])
        self.assertTrue(any("CORP_DARK_MATTER_SECRECY" in v for v in data["violations"]))
        self.assertTrue(any("CORP_CODE_TRUNCATION_PROHIBITED" in v for v in data["violations"]))

if __name__ == "__main__":
    unittest.main()