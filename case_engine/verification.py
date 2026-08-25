from __future__ import annotations

import json
import uuid

from openai import OpenAI

from .models import CaseMemory, Vulnerability
from .prompts import CONTRADICTION_PROMPT


def find_potential_contradictions(
    client: OpenAI,
    case: CaseMemory,
    model: str = "gpt-4o-mini",
) -> list[Vulnerability]:

    payload = {
        "facts": [
            {
                "fact_id": f.fact_id,
                "statement": f.statement,
                "date": f.date,
                "sources": f.sources,
            }
            for f in case.facts
        ],
        "timeline": [
            {
                "event_id": e.event_id,
                "date": e.date,
                "description": e.description,
                "fact_ids": e.fact_ids,
            }
            for e in case.timeline
        ],
    }

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": CONTRADICTION_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(
                    payload,
                    indent=2,
                ),
            },
        ],
    )

    result = json.loads(
        response.choices[0].message.content
    )

    return [
        Vulnerability(
            vulnerability_id=str(uuid.uuid4()),
            issue=item["issue"],
            severity=item.get("severity", "medium"),
            explanation=item["explanation"],
            related_fact_ids=item.get(
                "related_fact_ids",
                [],
            ),
            recommended_action=item.get(
                "recommended_action"
            ),
        )
        for item in result.get("contradictions", [])
    ]
