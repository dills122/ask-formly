"""Nonsemantic contract validation shared by both experimental planners."""
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Text = Annotated[str, StringConstraints(min_length=1, max_length=2000, pattern=r'\S')]
Detail = Annotated[str, StringConstraints(min_length=1, max_length=1000, pattern=r'\S')]
Code = Literal['invalid_input', 'capacity_exceeded', 'timeout', 'backend_error', 'invalid_output']


def validate_question(question: str) -> None:
    if not isinstance(question, str) or not 1 <= len(question) <= 8000 or not question.strip():
        raise ValueError('Question must contain 1–8000 codepoints and non-whitespace text')
    question.encode('utf-8')


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class Aspect(StrictModel):
    id: str
    requested_information: Text
    source_spans: list[list[int]] = Field(max_length=16)


class Request(StrictModel):
    id: str
    aspect_ids: list[str] = Field(min_length=1, max_length=8)
    query: Text
    context: str


class Ambiguity(StrictModel):
    description: Detail
    aspect_ids: list[str] = Field(max_length=8)


class Failure(StrictModel):
    code: Code
    detail: Detail


class Plan(StrictModel):
    schema_version: Literal[1]
    question: str
    status: Literal['planned', 'ambiguous', 'failed']
    aspects: list[Aspect] = Field(max_length=8)
    requests: list[Request] = Field(max_length=8)
    ambiguities: list[Ambiguity] = Field(max_length=8)
    failure: Failure | None

    @model_validator(mode='before')
    @classmethod
    def exact_schema_version(cls, value):
        if isinstance(value, dict) and type(value.get('schema_version')) is not int:
            raise ValueError('schema_version must be an integer')
        return value

    @model_validator(mode='after')
    def invariants(self):
        invalid_input = self.failure is not None and self.failure.code == 'invalid_input'
        if not invalid_input:
            validate_question(self.question)
        if self.status == 'failed':
            if self.failure is None or self.aspects or self.requests or self.ambiguities:
                raise ValueError('Failed plans require failure and empty result lists')
            return self
        if self.failure is not None:
            raise ValueError('Successful/ambiguous plans cannot contain failure')
        if self.status == 'planned' and (not self.aspects or not self.requests or self.ambiguities):
            raise ValueError('Planned status requires aspects/requests and no ambiguity')
        if self.status == 'ambiguous' and not self.ambiguities:
            raise ValueError('Ambiguous status requires ambiguity')
        ids = [a.id for a in self.aspects]
        if ids != [f'a{i+1}' for i in range(len(ids))]:
            raise ValueError('Aspect IDs must be unique and sequential')
        if [r.id for r in self.requests] != [f'q{i+1}' for i in range(len(self.requests))]:
            raise ValueError('Request IDs must be unique and sequential')
        covered = set()
        for request in self.requests:
            if request.context != self.question:
                raise ValueError('Original context must be exact')
            covered.update(request.aspect_ids)
        for linked in [*self.requests, *self.ambiguities]:
            if len(set(linked.aspect_ids)) != len(linked.aspect_ids) or not set(linked.aspect_ids) <= set(ids):
                raise ValueError('Invalid aspect references')
        if covered != set(ids):
            raise ValueError('Every aspect must have a request')
        for aspect in self.aspects:
            for span in aspect.source_spans:
                if len(span) != 2 or not 0 <= span[0] < span[1] <= len(self.question):
                    raise ValueError('Invalid codepoint span')
        return self


def make_plan(question: str, queries: list[str], ambiguities: list[str] | None = None) -> Plan:
    validate_question(question)
    ambiguities = [] if ambiguities is None else ambiguities
    return Plan(schema_version=1, question=question,
                status='ambiguous' if ambiguities else 'planned',
                aspects=[Aspect(id=f'a{i+1}', requested_information=q, source_spans=[])
                         for i, q in enumerate(queries)],
                requests=[Request(id=f'q{i+1}', aspect_ids=[f'a{i+1}'], query=q, context=question)
                          for i, q in enumerate(queries)],
                ambiguities=[Ambiguity(description=a, aspect_ids=[]) for a in ambiguities], failure=None)


def failed(question: str, code: Code, detail: str) -> Plan:
    return Plan(schema_version=1, question=question, status='failed', aspects=[], requests=[],
                ambiguities=[], failure=Failure(code=code, detail=detail[:1000] or code))
