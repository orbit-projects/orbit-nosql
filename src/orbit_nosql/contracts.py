# Copyright 2026-present Orbit Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Provider-neutral NoSQL resource contract built on Orbit's shared data repository."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from orbit_data import Repository
from pydantic import BaseModel

EntityT = TypeVar("EntityT", bound=BaseModel)
KeyT = TypeVar("KeyT", contravariant=True)


@runtime_checkable
class NoSQLDatabase(Protocol):
    """Create typed repositories for Pydantic models in logical collections.

    Implementations must validate collection names, avoid implicit schema creation unless
    documented, and return repositories that satisfy `orbit_data.Repository`. A returned
    repository is bound to the database resource and must not be used after it is closed.
    Transaction, query/filter, consistency and index behavior are provider-specific and must not
    be inferred from this contract. The database owns its client/pool and must release it from
    `aclose`; concurrent close calls must await the same cleanup, and caller cancellation must not
    interrupt resource release.
    """

    def repository(
        self,
        collection: str,
        model: type[EntityT],
        *,
        key_field: str = "id",
    ) -> Repository[EntityT, KeyT]:
        """Return a typed repository bound to one existing or provider-created collection."""

    async def aclose(self) -> None:
        """Idempotently release resources before propagating caller cancellation."""


__all__ = ["NoSQLDatabase"]
