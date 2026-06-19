---
source: blog
url: https://clickhouse.com/
topic: when-sigterm-does-nothing-a-postgres-mystery
ch_version_introduced: '01.458979'
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 10
---

`KnownAssignedXids` based on information from incoming WAL records. The function that implements the "wait for a transaction to complete" operation described earlier is named [`XactLockTableWait`](https://github.com/postgres/postgres/blob/483f7246f39b3af250fed1e613d962b85b568861/src/backend/storage/lmgr/lmgr.c#L663), and the crucial part for us is this loop (code simplified for brevity):

```
void
XactLockTableWait(TransactionId xid, Relation rel, ItemPointer ctid,
				  XLTW_Oper oper)
    <...>
	for (;;)
	{
		Assert(TransactionIdIsValid(xid));
		SET_LOCKTAG_TRANSACTION(tag, xid);

		(void) LockAcquire(&tag, ShareLock, false, false);
		LockRelease(&tag, ShareLock, false);

		if (!TransactionIdIsInProgress(xid))
			break;

        	pg_usleep(1000L);
	}
    <...>

```

Postgres acquires a lock on the transaction ID provided as input via `LockAcquire`, which hangs until the transaction completes and releases its lock. After obtaining the lock, we release it immediately and check if the transaction is still in progress via [`TransactionIdIsInProgress`](https://github.com/postgres/postgres/blob/7c319f54917faf564b660fe9027c4835a422bad6/src/backend/storage/ipc/procarray.c#L1402). If it isn't, we exit. However, there is a 1ms sleep before the loop repeats, which we hit if we find the transaction is still running. If we only reach the check after we acquire a lock, how can this happen? As mentioned in a comment within this function, there is a window where the transaction has registered itself as running but hasn't yet acquired its lock on the transactionid. While the code handles this case regardless, the sleep is good for avoiding repeated locking until the transaction reaches a consistent state. Under regular operation, this case should rarely be hit and not for very long.

![User Image (5).png](/uploads/User_Image_5_f945b563ad.png)
Let's now consider the case of a hot standby. A standby still needs to find a consistent point while creating a logical replication slot, and older transactions need to end for that. It isn't the one running the transaction; therefore, the `LockAcquire` will always return immediately on standby. But `TransactionIdIsInProgress` does take `KnownAssignedXids` into account, so we know that the transaction is still running. Thus, we hit the 1ms sleep and then another loop iteration. But unlike earlier, this is not a transient situation; we can be stuck here for hours.
