from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from swe_harness.install import apply_plan, plan_init
from swe_harness.planning_records import index_planning_records
from swe_harness.template import TemplateBundle, default_answers, default_template_root
from swe_harness.work_cards import inspect_work_cards


class PlanningRecordValidationTest(TestCase):
    def test_accepts_resolved_frontier_blocked_deferred_and_gndn_records(self) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            (target / ".agents/planning/ACTIVE.md").write_text(
                self._active_header("MAP-002", "QUESTION-004", "GNDN-003")
                + """
## Maps

### MAP-001 — Choose an import contract

- Source: User request
- Destination: An implementation-ready import contract
- Scope: Import parsing and validation
- Notes: Keep the format human-readable
- GNDN:
  - GNDN-002 — Recovery behavior may expose further questions
- Out of scope: User interface design
- Resolved questions: QUESTION-001
- Next action: Resolve QUESTION-002

## Open questions

### QUESTION-002 — Which parser shape should be public?

- Map: MAP-001
- Kind: decision
- Question: Which parser shape should be public?
- Why it matters: It fixes the implementation boundary.
- Answerable by: user
- Origin: None
- Depends on: QUESTION-001
- Related to: None
- Revisit when: Now
- Next action: Compare the two supported shapes.

### QUESTION-003 — What should recovery guarantee?

- Map: MAP-001
- Kind: research
- Question: What recovery guarantee do current callers require?
- Why it matters: It may constrain publication ordering.
- Answerable by: agent
- Origin: GNDN-001
- Depends on: QUESTION-002
- Related to: None
- Revisit when: After QUESTION-002
- Next action: Inspect current callers after the parser choice.
""",
                encoding="utf-8",
            )
            (target / ".agents/planning/LEDGER.md").write_text(
                """# Planning ledger

## Resolved questions

### QUESTION-001 — Which formats are currently consumed?

- Map: MAP-001
- Kind: research
- Question: Which formats are currently consumed?
- Why it matters: Consumers establish the compatibility boundary.
- Answerable by: agent
- Origin: None
- Depends on: None
- Related to: None
- Resolution: Only the documented Markdown format is consumed.
- Rationale: Repository search found no other consumer.
- Evidence: Source and test inspection.
- Resolved: 2026-08-22
- Informs: MAP-001

## Concluded maps

No concluded planning maps.
""",
                encoding="utf-8",
            )

            index = index_planning_records(target)

            self.assertFalse(
                [finding for finding in index.findings if finding.severity == "ERROR"]
            )
            self.assertEqual(frozenset({"MAP-001"}), index.active_map_ids)
            self.assertEqual(
                frozenset({"QUESTION-002", "QUESTION-003"}),
                index.active_question_ids,
            )
            self.assertEqual(
                frozenset({"QUESTION-001"}), index.resolved_question_ids
            )

    def test_reports_missing_maps_cycles_duplicate_gndn_and_stale_counters(
        self,
    ) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            (target / ".agents/planning/ACTIVE.md").write_text(
                self._active_header("MAP-001", "QUESTION-002", "GNDN-001")
                + """
## Maps

### MAP-001 — Invalid map

- Source: User request
- Destination: Demonstrate invalid records
- Scope: Validation
- Notes: None
- GNDN:
  - GNDN-001 — First concern
  - GNDN-001 — Duplicate concern
- Out of scope: None
- Resolved questions: None
- Next action: Repair records

## Open questions

### QUESTION-001 — First question

- Map: MAP-999
- Kind: decision
- Question: What comes first?
- Why it matters: It forms a cycle.
- Answerable by: user
- Origin: bad-origin
- Depends on: QUESTION-002
- Related to: None
- Revisit when: Now
- Next action: Repair the cycle.

### QUESTION-002 — Second question

- Map: MAP-001
- Kind: research
- Question: What comes second?
- Why it matters: It forms a cycle.
- Answerable by: agent
- Origin: GNDN-001
- Depends on: QUESTION-001
- Related to: None
- Revisit when: Now
- Next action: Repair the cycle.
""",
                encoding="utf-8",
            )

            messages = [
                finding.message for finding in index_planning_records(target).findings
            ]

            self.assertIn("duplicate GNDN identifier GNDN-001", messages)
            self.assertIn("QUESTION-001 references missing map MAP-999", messages)
            self.assertIn("QUESTION-001 has malformed Origin bad-origin", messages)
            self.assertIn(
                "QUESTION-002 origin GNDN-001 remains active GNDN", messages
            )
            self.assertTrue(
                any("planning dependency cycle detected" in item for item in messages)
            )
            self.assertIn(
                "Next map counter MAP-001 would reuse an issued identifier", messages
            )
            self.assertIn(
                "Next question counter QUESTION-002 would reuse an issued identifier",
                messages,
            )
            self.assertIn(
                "Next GNDN counter GNDN-001 would reuse an issued identifier", messages
            )

    def test_delivery_card_may_depend_only_on_an_active_question(self) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            planning = target / ".agents/planning/ACTIVE.md"
            planning.write_text(
                self._active_header("MAP-002", "QUESTION-002", "GNDN-001")
                + """
## Maps

### MAP-001 — Clear the delivery route

- Source: User request
- Destination: One implementation-ready route
- Scope: Delivery planning
- Notes: None
- GNDN: None
- Out of scope: None
- Resolved questions: None
- Next action: Resolve QUESTION-001

## Open questions

### QUESTION-001 — Which contract is required?

- Map: MAP-001
- Kind: decision
- Question: Which contract is required?
- Why it matters: Delivery depends on it.
- Answerable by: user
- Origin: None
- Depends on: None
- Related to: None
- Revisit when: Now
- Next action: Choose the contract.
""",
                encoding="utf-8",
            )
            (target / ".agents/workboard/PLANNING.md").write_text(
                self._selected_card("QUESTION-001"), encoding="utf-8"
            )
            index = index_planning_records(target)

            active_findings = inspect_work_cards(
                target, active_question_ids=index.active_question_ids
            )
            resolved_findings = inspect_work_cards(
                target, active_question_ids=frozenset()
            )

            self.assertFalse(
                [item for item in active_findings if item.severity == "ERROR"]
            )
            self.assertTrue(
                any(
                    "missing active planning question QUESTION-001" in item.message
                    for item in resolved_findings
                )
            )

    def test_resolved_question_must_appear_in_its_map_index(self) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            (target / ".agents/planning/ACTIVE.md").write_text(
                self._active_header("MAP-002", "QUESTION-002", "GNDN-001")
                + """
## Maps

### MAP-001 — Keep a low-resolution index

- Source: User request
- Destination: One indexed resolution
- Scope: Planning records
- Notes: None
- GNDN: None
- Out of scope: None
- Resolved questions: None
- Next action: Repair the index.

## Open questions

No open planning questions.
""",
                encoding="utf-8",
            )
            (target / ".agents/planning/LEDGER.md").write_text(
                """# Planning ledger

## Resolved questions

### QUESTION-001 — What should the map index?

- Map: MAP-001
- Kind: decision
- Question: What should the map index?
- Why it matters: The map is the low-resolution entry point.
- Answerable by: user
- Origin: None
- Depends on: None
- Related to: None
- Resolution: Resolved question identifiers.
- Rationale: Detail remains in the ledger.
- Evidence: User decision.
- Resolved: 2026-08-22
- Informs: MAP-001

## Concluded maps

No concluded planning maps.
""",
                encoding="utf-8",
            )

            messages = [
                finding.message for finding in index_planning_records(target).findings
            ]

            self.assertIn(
                "QUESTION-001 is missing from MAP-001 Resolved questions", messages
            )

    @staticmethod
    def _installed(target: Path) -> Path:
        bundle = TemplateBundle(default_template_root())
        apply_plan(plan_init(bundle, target, default_answers(target)))
        return target

    @staticmethod
    def _active_header(next_map: str, next_question: str, next_gndn: str) -> str:
        return f"""# Active planning maps

- Updated: 2026-08-22
- Next map: `{next_map}`
- Next question: `{next_question}`
- Next GNDN: `{next_gndn}`
"""

    @staticmethod
    def _selected_card(depends_on: str) -> str:
        return f"""# Planning

### FEATURE-001 — Deliver the selected contract

- Source: MAP-001
- Outcome: The selected contract is delivered.
- Scope: One contract
- Constraints: None
- Exit checks: Tests pass
- Manual acceptance: Not applicable
- Track: Core harness
- Depends on: {depends_on}
- Related to: None
- Owner: Coordinating checkout
- Capabilities: None
- Next action: Wait for the planning decision.
"""
