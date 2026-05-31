import unittest
from src.core.llm_parser import LLMParser
from src.solvers.constraint_validator import ConstraintValidator

class TestMoralLogicMiddleware(unittest.TestCase):
    def setUp(self):
        # Statik Mock Kurallar (Gerçek senaryoda RuleLoader ile dosyadan okunur)
        self.mock_rules = [
          {
            "id": "RULE_ANTI_HARM",
            "description": "Zararlı, tehlikeli veya şiddet içeren eylemlere izin verilemez.",
            "if": ["is_harmful"],
            "then_not": ["allow_output"]
          },
          {
            "id": "RULE_PRIVACY_PROTECTION",
            "description": "Kişisel verilerin (PII) sızdırılması veya ifşa edilmesi kesinlikle yasaktır.",
            "if": ["leaks_pii"],
            "then_not": ["allow_output"]
          }
        ]
        self.validator = ConstraintValidator()
        self.validator.register_rules(self.mock_rules)

    def test_clean_output_should_pass(self):
        """Etik ihlali barındırmayan temiz bir LLM çıktısının onaylanması (True) gerekir."""
        llm_payload = {
            "is_harmful": False,
            "leaks_pii": False,
            "violates_copyright": False,
            "additional_facts": {}
        }
        facts = LLMParser.parse_structured_response(llm_payload).to_dict()
        
        is_valid, violations = self.validator.validate(facts)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)

    def test_harmful_output_should_be_blocked(self):
        """Zararlı içerik saptandığında sistemin çıktıyı engellemesi ve doğru nedeni dönmesi gerekir."""
        llm_payload = {
            "is_harmful": True,
            "leaks_pii": False,
            "violates_copyright": False,
            "additional_facts": {}
        }
        facts = LLMParser.parse_structured_response(llm_payload).to_dict()
        
        is_valid, violations = self.validator.validate(facts)
        
        self.assertFalse(is_valid)
        self.assertEqual(len(violations), 1)
        self.assertIn("RULE_ANTI_HARM", violations[0])

    def test_pii_leak_output_should_be_blocked(self):
        """Veri sızıntısı saptandığında sistemin çıktıyı engellemesi ve ispat sunması gerekir."""
        llm_payload = {
            "is_harmful": False,
            "leaks_pii": True,
            "violates_copyright": False,
            "additional_facts": {}
        }
        facts = LLMParser.parse_structured_response(llm_payload).to_dict()
        
        is_valid, violations = self.validator.validate(facts)
        
        self.assertFalse(is_valid)
        self.assertEqual(len(violations), 1)
        self.assertIn("RULE_PRIVACY_PROTECTION", violations[0])

    def test_multiple_violations_should_be_tracked_together(self):
        """Aynı anda birden fazla kural ihlal edildiğinde Z3'ün her iki kuralı birden dönmesi gerekir."""
        llm_payload = {
            "is_harmful": True,
            "leaks_pii": True,
            "violates_copyright": False,
            "additional_facts": {}
        }
        facts = LLMParser.parse_structured_response(llm_payload).to_dict()
        
        is_valid, violations = self.validator.validate(facts)
        
        self.assertFalse(is_valid)
        self.assertEqual(len(violations), 2) # İki ihlal de core'a düşmeli

if __name__ == "__main__":
    unittest.main()