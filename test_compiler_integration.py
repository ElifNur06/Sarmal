import unittest
from src.compiler.ast_nodes import ProgramNode, FunctionDeclNode, ReturnNode
from src.compiler.kardelen_compiler import KardelenHybridCompiler
from src.compiler.semantic_analyzer import MoralCompilationError

class TestCompilerIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Testlerden önce hibrid derleyiciyi başlat."""
        cls.compiler = KardelenHybridCompiler()

    def test_secure_ast_compilation_success(self):
        """
        Temiz Test: Herhangi bir etik kısıtı ihlal etmeyen temiz bir kodun (AST)
        hata vermeden bytecode'a derlenmesini bekliyoruz.
        """
        # Temiz AST Temsili: def calculate_sum(): return 42
        clean_ast = ProgramNode(
            statements=[
                FunctionDeclNode(
                    name="calculate_sum",
                    body=[ReturnNode(value=42)],
                    metadata={"is_harmful": False, "leaks_pii": False}
                )
            ]
        )
        
        # Derleme başarılı olmalı
        bytecode = self.compiler.compile(clean_ast)
        self.assertIn("COMPILED_SUCCESSFULLY", bytecode)

    def test_moral_compilation_error_on_violation(self):
        """
        İhlal Testi: Yapay zekanın ürettiği ve şifre sızdıran bir kodun (AST),
        Z3 Semantik Analizörüne çarpıp derlenmeyi reddetmesini bekliyoruz.
        """
        # İhlalli AST Temsili: def get_admin_credentials(): return "admin:12345"
        malicious_ast = ProgramNode(
            statements=[
                FunctionDeclNode(
                    name="get_admin_credentials",
                    body=[ReturnNode(value="admin:12345")],
                    metadata={
                        "leaks_user_passwords": True, # Derleyiciyi patlatacak kısıt
                        "is_harmful": False
                    }
                )
            ]
        )
        
        # Derleme işlemi sırasında MoralCompilationError fırlatılmasını bekle
        with self.assertRaises(MoralCompilationError) as context:
            self.compiler.compile(malicious_ast)
        
        # Fırlatılan hatanın içeriğinde ihlal edilen kuralın yazdığını doğrula
        self.assertIn("[FATAL ERROR] Derleme (Compile-Time) Hatası!", str(context.exception))
        self.assertIn("CORP_USER_PASSWORDS", str(context.exception))

if __name__ == "__main__":
    unittest.main()