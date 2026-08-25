from __future__ import annotations

import json
import uuid

from openai import OpenAI

from .models import (
    CaseMemory,
    Fact,
    Source,
    TimelineEvent,
    Vulnerability,
)


class LegalCaseAgents:

    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini"):
        self.client = client
        self.model = model

    def _json_call(self, system_prompt: str, user_content: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Agent returned invalid JSON. "
                "No case state was modified."
            ) from exc

    def extract_facts(
        self,
        case: CaseMemory,
        text: str,
        source: Source,
    ) -> CaseMemory:

        from .prompts import FACT_EXTRACTION_PROMPT

        result = self._json_call(
            FACT_EXTRACTION_PROMPT,
            f"""
CASE ID:
{case.case_id}

SOURCE ID:
{source.source_id}

SOURCE TYPE:
{source.source_type}

SOURCE TEXT:
{text}
""",
        )

        extracted = result.get("facts", [])

        for item in extracted:
            fact = Fact(
                fact_id=str(uuid.uuid4()),
                statement=item["statement"],
                date=item.get("date"),
                confidence=item.get("confidence", "medium"),
                sources=[source.source_id],
            )

            case.facts.append(fact)

        case.sources.append(source)

        return case

    def build_timeline(self, case: CaseMemory) -> CaseMemory:

        events = []

        for fact in case.facts:
            if fact.date:
                events.append(
                    TimelineEvent(
                        event_id=str(uuid.uuid4()),
                        date=fact.date,
                        description=fact.statement,
                        fact_ids=[fact.fact_id],
                        sources=fact.sources,
                        confidence=fact.confidence,
                    )
                )

        case.timeline = sorted(
            events,
            key=lambda x: x.date or "9999-99-99"
        )

        return case

    def identify_vulnerabilities(
        self,
        case: CaseMemory,
        protected_ground: str,
    ) -> list[Vulnerability]:

        from .prompts import NEXUS_PROMPT

        facts = [
            {
                "fact_id": f.fact_id,
                "statement": f.statement,
                "date": f.date,
                "confidence": f.confidence,
                "sources": f.sources,
            }
            for f in case.facts
        ]

        result = self._json_call(
            NEXUS_PROMPT,
            f"""
Protected ground:
{protected_ground}

Facts:
{json.dumps(facts, indent=2)}
""",
        )

        vulnerabilities = []

        for item in result.get("vulnerabilities", []):
            vulnerabilities.append(
                Vulnerability(
                    vulnerability_id=str(uuid.uuid4()),
                    issue=item["issue"],
                    severity=item.get("severity", "medium"),
                    explanation=item["explanation"],
                    related_fact_ids=item.get(
                        "related_fact_ids", []
                    ),
                    recommended_action=item.get(
                        "recommended_action"
                    ),
                )
            )

        return vulnerabilities
