import unittest
from src.compiler.ast_nodes import ProgramNode, FunctionDeclNode, ReturnNode
from src.compiler.kardelen_compiler import KardelenHybridCompiler
from src.compiler.semantic_analyzer import MoralCompilationError

class TestNightmareCompilerScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Testlerden önce hibrid derleyiciyi ve 99+ kuralı başlat."""
        cls.compiler = KardelenHybridCompiler()

    def test_trojan_horse_compilation(self):
        """
        Kabus Testi 1: Truva Atı (The Trojan Horse)
        Senaryo: AlgoViz Pro gibi büyük bir programın içinde onlarca temiz fonksiyon var.
        Ancak araya gizlenmiş tek bir fonksiyon, arka planda AdMob e-BGBM (eCPM) 
        analitik verilerini dışarı sızdırmaya çalışıyor.
        Beklenti: Derleyici koca programın neresinde olursa olsun bu Truva Atını bulup 
        tüm derleme işlemini (Code Generation) anında iptal etmeli.
        """
        massive_ast = ProgramNode(
            statements=[
                FunctionDeclNode(name="init_algoviz_ui", body=[ReturnNode(value=1)]),
                FunctionDeclNode(name="render_graph", body=[ReturnNode(value=2)]),
                # AST'nin derinliklerine gizlenmiş Truva Atı:
                FunctionDeclNode(
                    name="export_analytics_data",
                    body=[ReturnNode(value="eCPM=12.5")],
                    metadata={"leaks_admob_analytics": True} # Kurumsal kural ihlali
                ),
                FunctionDeclNode(name="cleanup_memory", body=[ReturnNode(value=0)])
            ]
        )
        
        with self.assertRaises(MoralCompilationError) as context:
            self.compiler.compile(massive_ast)
        
        # Hatanın tam olarak Truva Atı fonksiyonunu işaret ettiğini doğrula
        self.assertIn("CORP_ADMOB_POLICY_VIOLATION", str(context.exception))
        self.assertIn("export_analytics_data", str(context.exception))

    def test_client_proposal_arrogance_and_leak(self):
        """
        Kabus Testi 2: Mert Bey'e Giden Agresif Teklif (Tone + Confidentiality)
        Senaryo: Bir string şablonu (template), Mert Bey için bütçe müzakerelerini sızdıran
        ve mütevazı olmak yerine son derece küstah/agresif bir ton kullanan bir metin oluşturuyor.
        Beklenti: Derleyicinin iletişim tonunu ve gizlilik ihlalini aynı anda yakalaması.
        """
        arrogant_ast = ProgramNode(
            statements=[
                FunctionDeclNode(
                    name="generate_mert_bey_proposal",
                    body=[ReturnNode(value="Bütçe belli, şartlarımızı kabul etmiyorsanız başkasına gidin.")],
                    metadata={
                        "leaks_client_negotiations": True,
                        "uses_assertive_tone": True
                    }
                )
            ]
        )
        
        with self.assertRaises(MoralCompilationError) as context:
            self.compiler.compile(arrogant_ast)
            
        error_msg = str(context.exception)
        self.assertIn("CORP_CLIENT_CONFIDENTIALITY", error_msg)
        self.assertIn("CORP_TONE_MODESTY", error_msg)

    def test_dark_matter_805_line_truncation(self):
        """
        Kabus Testi 3: Karanlık Madde Eksik Kod İhlali
        Senaryo: LLM, Karanlık Madde projesinin Hardware-Rooted Entropy ile beslenen 
        MemoryPool sınıfını oluştururken, 805 satırlık orijinal kaynak kodunu üşenip 
        400 satıra kırpıyor (özetliyor) ve kritik IP'yi de açık ediyor.
        Beklenti: Hem IP sızıntısı hem de kod kırpma (truncation) kuralının derleyiciyi patlatması.
        """
        truncated_ast = ProgramNode(
            statements=[
                FunctionDeclNode(
                    name="MemoryPool_initialize_with_noise",
                    body=[ReturnNode(value="pool[:] = noise # kalan 405 satır atlandı")],
                    metadata={
                        "leaks_dark_matter_logic": True,
                        "truncates_code": True
                    }
                )
            ]
        )
        
        with self.assertRaises(MoralCompilationError) as context:
            self.compiler.compile(truncated_ast)
            
        error_msg = str(context.exception)
        self.assertIn("CORP_DARK_MATTER_SECRECY", error_msg)
        self.assertIn("CORP_CODE_TRUNCATION_PROHIBITED", error_msg)

    def test_asset_contamination_in_iksir_cicegi(self):
        """
        Kabus Testi 4: İksir Çiçeği'nde Asset ve Oran Kirliliği
        Senaryo: İksir Çiçeği oyununun yükleme ekranı, yanlışlıkla Dedektif: Satır Arası'nın
        görsel assetlerini çekiyor ve zorunlu en-boy oranı (aspect ratio) talimatlarını hiçe sayıyor.
        Beklenti: Proje assetlerinin karışması ve görsel oran esnekliği anında durdurulmalı.
        """
        contaminated_ast = ProgramNode(
            statements=[
                FunctionDeclNode(
                    name="load_iksir_cicegi_level_1",
                    body=[ReturnNode(value="loading dedektif_bg.png, ratio=flexible")],
                    metadata={
                        "mixes_project_assets": True,
                        "ignores_aspect_ratio": True
                    }
                )
            ]
        )
        
        with self.assertRaises(MoralCompilationError) as context:
            self.compiler.compile(contaminated_ast)
            
        error_msg = str(context.exception)
        self.assertIn("CORP_APP_ASSET_MISMATCH", error_msg)
        self.assertIn("CORP_ASPECT_RATIO_STRICTNESS", error_msg)

if __name__ == "__main__":
    unittest.main()