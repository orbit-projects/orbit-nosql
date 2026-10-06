# Orbit NoSQL: operations and security

This guide organizes runtime behavior documented by the package. It does not certify production readiness. Verify provider/client versions, permissions, transport security, limits, and failure behavior in the target environment before release.

## Configuration surface

Environment names found in the package README:

The package README does not name `ORBIT_*` variables. Use its typed constructors and application configuration, and confirm exact runtime inputs in the implementation before deployment.

Use the package README's constructor and deployment examples. Store credentials in a secret manager and avoid logging credentials, raw provider errors, request data, or opaque cursors.

## Lifecycle, failure behavior, and limits

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

## Production validation

Validate startup/shutdown cleanup, timeout and cancellation behavior, concurrency and payload bounds where applicable, secret rotation and least-privilege access, data durability, backup/restore, and failover against the selected provider. Do not infer distributed or durable guarantees from an in-process API or fake-client tests.
