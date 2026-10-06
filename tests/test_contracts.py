"""Structural contract tests for NoSQL provider resources."""

from typing import get_args, get_origin, get_type_hints

from orbit_data import Repository

from orbit_nosql import NoSQLDatabase


class _Database:
    def repository(self, collection, model, *, key_field="id"):
        raise NotImplementedError

    async def aclose(self):
        return None


def test_database_protocol_is_structural() -> None:
    """NoSQL adapters satisfy the contract without inheriting implementation classes."""
    assert isinstance(_Database(), NoSQLDatabase)
    result = get_type_hints(NoSQLDatabase.repository)["return"]
    assert get_origin(result) is Repository
    assert len(get_args(result)) == 2
