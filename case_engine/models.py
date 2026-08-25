from __future__ import annotations

from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high", "critical"]
Confidence = Literal["low", "medium", "high"]
SourceType = Literal[
    "client_statement",
    "voice_note",
    "document",
    "email",
    "whatsapp",
    "legal_authority",
    "other",
]


class Source(BaseModel):
    source_id: str
    source_type: SourceType
    name: str
    location: Optional[str] = None
    excerpt: Optional[str] = None


class Fact(BaseModel):
    fact_id: str
    statement: str
    date: Optional[str] = None
    confidence: Confidence = "medium"
    sources: list[str] = Field(default_factory=list)
    attorney_verified: bool = False


class TimelineEvent(BaseModel):
    event_id: str
    date: Optional[str] = None
    description: str
    fact_ids: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    confidence: Confidence = "medium"


class EvidenceItem(BaseModel):
    evidence_id: str
    description: str
    evidence_type: str
    supports_fact_ids: list[str] = Field(default_factory=list)
    source_id: Optional[str] = None
    status: Literal[
        "identified",
        "requested",
        "received",
        "verified",
        "missing",
    ] = "identified"


class LegalAuthority(BaseModel):
    authority_id: str
    citation: str
    proposition: str
    jurisdiction: Optional[str] = None
    source_url: Optional[str] = None
    verified: bool = False
    verification_notes: Optional[str] = None


class Vulnerability(BaseModel):
    vulnerability_id: str
    issue: str
    severity: Severity
    explanation: str
    related_fact_ids: list[str] = Field(default_factory=list)
    recommended_action: Optional[str] = None


class CaseMemory(BaseModel):
    case_id: str
    case_type: str = "Humanitarian Immigration"
    applicant_name: Optional[str] = None
    country_of_origin: Optional[str] = None

    sources: list[Source] = Field(default_factory=list)
    facts: list[Fact] = Field(default_factory=list)
    timeline: list[TimelineEvent] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    authorities: list[LegalAuthority] = Field(default_factory=list)
    vulnerabilities: list[Vulnerability] = Field(default_factory=list)

    attorney_approved: bool = False
