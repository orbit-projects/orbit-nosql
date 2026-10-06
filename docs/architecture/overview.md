# Orbit NoSQL: architecture and boundaries

## Responsibility

`orbit-nosql` is the provider-neutral NoSQL capability layer. `orbit-data` remains the common
repository contract shared by SQL and NoSQL implementations. This initial version uses Pydantic
models as its entity type and defines how an application obtains an `orbit_data.Repository` for a
named logical collection without importing a vendor driver.

Providers live in separate packages. `orbit-nosql-mongo` supplies a document collection implementation;
`orbit-cache-redis` may expose a key-value backed repository alongside its separate cache capability.
The capability does not claim that transactions, secondary indexes, query languages, consistency,
or collection semantics are identical across NoSQL systems. Provider-specific features remain
explicit on their provider packages.

```python
from pydantic import BaseModel
from orbit_nosql import NoSQLDatabase


class Session(BaseModel):
    id: str
    owner_id: str


async def load_session(database: NoSQLDatabase, session_id: str) -> Session | None:
    sessions = database.repository("sessions", Session)
    return await sessions.get(session_id)
```

The returned repository follows `orbit-data` CRUD semantics. This capability does not promise
cross-provider query languages, transaction support, index management, or consistent pagination.
Provider plugins own client startup and shutdown; close a directly constructed database with
`await database.aclose()`. Closing is idempotent. Concurrent close callers wait for the same
cleanup, and cancellation of a caller is propagated only after its owned resource cleanup finishes.
Repositories obtained from a database are only valid while that database resource remains open.

```bash
pip install orbit-data orbit-nosql orbit-nosql-mongo
```

This package is pre-alpha; its API is not stable. It supports Python 3.11 through 3.14. Its
provider-neutral contract test passes on all four supported Python versions.

Licensed under Apache-2.0.

## Declared dependencies

The following dependency declarations come from the checked-in manifests. Optional groups and development dependencies are called out separately.

### `pyproject.toml`
- `orbit-data>=0.1.0a1,<0.2`
- `pydantic>=2.8,<3`
- Optional `dev` group: `pytest>=8,<10`, `ruff>=0.8,<1`, `mypy>=1.13,<2`.

Declared dependencies do not mean that optional providers or services are bundled with this package.

## Implementation layout

Representative implementation files in this checkout:

- `src/orbit_nosql/__init__.py`
- `src/orbit_nosql/contracts.py`

## Public contract and scope

The README does not contain a separately headed architecture section. Its responsibility statement above and the public source files define the implemented scope; this guide adds no behavior beyond that description.

## Boundary rules

Keep provider SDKs, credentials, transports, and provider-specific error translation in provider adapters. Keep reusable capability contracts in the matching capability package and lifecycle orchestration in Core. Apply the relevant layer for this repository and preserve the dependency direction shown above.
