from domain.model.sample import Sample
from infrastructure.output.postgresql.entity.sample_entity import SampleEntity
from infrastructure.output.postgresql.mapper.client_entity_mapper import (
    ClientEntityMapper,
)
from infrastructure.output.postgresql.mapper.sample_type_entity_mapper import (
    SampleTypeEntityMapper,
)


class SampleEntityMapper:
    def __init__(
        self,
        sample_type_entity_mapper: SampleTypeEntityMapper,
        client_entity_mapper: ClientEntityMapper,
    ):
        self.sample_type_entity_mapper = sample_type_entity_mapper
        self.client_entity_mapper = client_entity_mapper

    def to_entity(self, sample: Sample) -> SampleEntity:
        return SampleEntity(
            id=sample.id,
            sample_code=sample.sample_code,
            sample_type_id=sample.sample_type.id,
            client_id=sample.client.id,
            get_sample_date=sample.get_sample_date,
            reception_date=sample.reception_date,
            analysis_date=sample.analysis_date,
            sample_location=sample.sample_location,
            responsable=sample.responsable,
        )

    def to_domain(self, entity: SampleEntity) -> Sample | None:
        if entity:
            return Sample(
                id=entity.id,
                sample_code=entity.sample_code,
                sample_type=self.sample_type_entity_mapper.to_domain(
                    entity.sample_type
                ),
                client=self.client_entity_mapper.to_domain(entity.client),
                get_sample_date=entity.get_sample_date,
                reception_date=entity.reception_date,
                analysis_date=entity.analysis_date,
                sample_location=entity.sample_location,
                responsable=entity.responsable,
            )
        return None

    def to_domain_list(self, entities: list[SampleEntity]) -> list[Sample]:
        return [self.to_domain(entity) for entity in entities]
