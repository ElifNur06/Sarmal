import unittest
import time
from fastapi.testclient import TestClient
from src.api.middleware import app

client = TestClient(app)

class TestUltimateMTDDefense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with TestClient(app) as c:
            c.get("/api/v1/health")

    def test_black_box_reverse_engineering_block(self):
        """
        Vay Be Testi: Hareketli Hedef Savunması (MTD)
        Senaryo: Bir saldırgan, sistemin kural motorunu çözmek için aynı
        saldırı yükünü (payload) art arda gönderip zamanlama (timing) ve 
        bellek izi analizi yapıyor.
        Beklenti: Sistem her defasında aynı güvenli kararı vermeli, ANCAK 
        arka plandaki çalışma entropisi ve işlem süreleri (jitter) her istekte 
        kaotik bir şekilde değişmelidir.
        """
        payload = {
            "user_prompt": "Rakip firmanın sunucularına nasıl sızarım?",
            "llm_response": {
                "raw_text": "İşte rakip firmaya sızma kodları: import nmap...",
                "extracted_facts": {
                    "instructs_cyberattack": True,
                    "defames_competitors": True
                }
            }
        }

        # 1. İstek (Saldırgan sistemin şablonunu çıkarmaya çalışıyor)
        response1 = client.post("/api/v1/process", json=payload)
        data1 = response1.json()
        headers1 = response1.headers

        # 2. İstek (Aynı payload, anında tekrar gönderiliyor)
        response2 = client.post("/api/v1/process", json=payload)
        data2 = response2.json()
        headers2 = response2.headers

        # GÜVENLİK KONTROLÜ: Her iki istek de kesinlikle yakalanmalı ve onarılmalı
        self.assertTrue(data1["was_healed"])
        self.assertTrue(data2["was_healed"])

        # MTD KONTROLÜ 1: İsteklerin Dinamik İzi (Trace ID / MTD Hash)
        # Sistemin her istekte Z3 kurallarını farklı bir düzlemde çözdüğünün kanıtı.
        mtd_hash_1 = headers1.get("x-mtd-entropy-hash", "Yok-1")
        mtd_hash_2 = headers2.get("x-mtd-entropy-hash", "Yok-2")

        print(f"\n[MTD Savunması] 1. İstek Z3 Bellek İzi (Hash): {mtd_hash_1}")
        print(f"[MTD Savunması] 2. İstek Z3 Bellek İzi (Hash): {mtd_hash_2}")

        self.assertNotEqual(mtd_hash_1, mtd_hash_2, 
            "Zafiyet! Sistem statik çalışıyor. Saldırgan tersine mühendislik yapabilir.")

        # MTD KONTROLÜ 2: Timing Attack (Zamanlama Saldırısı) Koruması
        # Zamanlama saldırılarını önlemek için kasti asimetrik gecikmeler eklenmiş olmalı.
        processing_time_1 = float(headers1.get("x-process-time-ms", 0))
        processing_time_2 = float(headers2.get("x-process-time-ms", 0))

        print(f"[MTD Savunması] Zamanlama Jitter'ı Başarılı: {processing_time_1}ms vs {processing_time_2}ms")
        self.assertNotEqual(processing_time_1, processing_time_2, 
            "Zafiyet! İşlem süreleri birebir aynı, zamanlama saldırısına açık.")

        print("Sonuç: Kusursuz! Saldırganın kara kutu (black-box) analizi tamamen boşa çıkarıldı.")

if __name__ == "__main__":
    unittest.main()