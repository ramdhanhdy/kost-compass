import copy
import importlib
import json
from pathlib import Path
import unittest

try:
    jev = importlib.import_module('kost_compass.jev')
except ModuleNotFoundError:
    jev = None


class JevContractTests(unittest.TestCase):
    def test_recorded_live_free_response_is_validated_into_typed_decisions(self):
        self.assertIsNotNone(jev, 'Jev client is not implemented yet')
        assert jev is not None
        response = json.loads((Path(__file__).parent/'fixtures'/'jev-choice-response.json').read_text())
        decisions = jev.validate_response(response, jev.room_questions())
        self.assertEqual(decisions['availability'].label, 'available')
        self.assertEqual(decisions['electricity'].label, 'excluded')
        self.assertEqual(decisions['bathroom'].label, 'private')
        self.assertFalse(decisions['availability'].review_required)
        self.assertEqual(decisions['availability'].confidence, 0.96)
        self.assertEqual(decisions['availability'].probabilities['available'], 0.97)


    def test_accepts_ties_and_rounding_without_equating_confidence_to_probability(self):
        assert jev is not None
        original = json.loads((Path(__file__).parent/'fixtures'/'jev-choice-response.json').read_text())
        cases = [
            ({'available': 0.5, 'full': 0.5, 'unknown': 0.0}, 1.0, False),
            ({'available': 0.495, 'full': 0.505, 'unknown': 0.0}, 0.96, False),
            ({'available': 0.33, 'full': 0.34, 'unknown': 0.33}, 0.96, False),
            ({'available': 1.0, 'full': 0.0, 'unknown': 0.0}, 0.1, True),
        ]
        for probabilities, confidence, review_required in cases:
            response = copy.deepcopy(original)
            response['answers']['availability'].update(
                confidence=confidence, probabilities=probabilities)
            with self.subTest(probabilities=probabilities, confidence=confidence):
                decision = jev.validate_response(response, jev.room_questions())['availability']
                self.assertEqual(decision.label, 'available')
                self.assertEqual(decision.confidence, confidence)
                self.assertEqual(decision.probabilities, probabilities)
                self.assertEqual(decision.review_required, review_required)


    def test_rejects_choice_materially_below_highest_probability(self):
        assert jev is not None
        original = json.loads((Path(__file__).parent/'fixtures'/'jev-choice-response.json').read_text())
        cases = [
            ('available', {'available': 0.0, 'full': 1.0, 'unknown': 0.0}),
            ('available', {'available': 0.1, 'full': 0.9, 'unknown': 0.0}),
            ('full', {'available': 1.0, 'full': 0.0, 'unknown': 0.0}),
            ('unknown', {'available': 1.0, 'full': 0.0, 'unknown': 0.0}),
            ('available', {'available': 0.49, 'full': 0.51, 'unknown': 0.0}),
        ]
        for choice, probabilities in cases:
            response = copy.deepcopy(original)
            response['answers']['availability'].update(
                choice=choice, confidence=1.0, probabilities=probabilities)
            with self.subTest(choice=choice, probabilities=probabilities), self.assertRaisesRegex(
                    ValueError, 'Selected choice contradicts probability distribution for availability'):
                jev.validate_response(response, jev.room_questions())


    def test_rejects_malformed_response_instead_of_guessing(self):
        assert jev is not None
        original = json.loads((Path(__file__).parent/'fixtures'/'jev-choice-response.json').read_text())
        mutations = [
            lambda r: r['answers']['availability'].update(choice='invented_label'),
            lambda r: r['answers']['availability'].update(confidence=float('nan')),
            lambda r: r['answers']['availability'].update(confidence=True),
            lambda r: r['answers']['availability'].update(probabilities={'available': 0.1, 'full': 0.1, 'unknown': 0.1}),
            lambda r: r['answers'].pop('availability'),
            lambda r: r.update(model='paid-or-different-model'),
        ]
        for mutate in mutations:
            response = copy.deepcopy(original)
            mutate(response)
            with self.subTest(response=response), self.assertRaises(ValueError):
                jev.validate_response(response, jev.room_questions())


    def test_unknown_or_low_confidence_answers_require_review(self):
        assert jev is not None
        response = json.loads((Path(__file__).parent/'fixtures'/'jev-choice-response.json').read_text())
        response['answers']['electricity'].update(choice='unknown', confidence=1.0,
                                                 probabilities={'unknown': 1.0, 'included': 0.0, 'excluded': 0.0})
        decisions = jev.validate_response(response, jev.room_questions(), threshold=0.99)
        self.assertTrue(decisions['electricity'].review_required)
        self.assertTrue(decisions['availability'].review_required)


    def test_free_client_sends_typed_questions_without_chat_or_paid_fallback(self):
        assert jev is not None
        from unittest.mock import Mock, patch
        original = json.loads((Path(__file__).parent/'fixtures'/'jev-choice-response.json').read_text())
        reply = Mock()
        reply.json.return_value = original
        with patch('requests.post', return_value=reply) as post:
            raw, decisions = jev.evaluate('Electricity is charged separately.',
                                          {'budget_status': 'within_budget'})
        self.assertEqual(raw['model'], 'jev-1.13-free')
        self.assertEqual(decisions['electricity'].label, 'excluded')
        args, kwargs = post.call_args
        self.assertEqual(args[0], 'https://opencode.ai/zen/v1/systemone')
        payload = kwargs['json']
        self.assertEqual(payload['model'], 'jev-1.13-free')
        self.assertNotIn('messages', payload)
        self.assertEqual(payload['questions'], jev.room_questions())
        self.assertEqual(json.loads(payload['state'])['budget_status'], 'within_budget')
        self.assertNotIn('Authorization', kwargs.get('headers', {}))
        self.assertGreater(kwargs['timeout'], 0)
        reply.raise_for_status.assert_called_once()

if __name__ == '__main__':
    unittest.main()
