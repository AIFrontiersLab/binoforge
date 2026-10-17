# Operation identity

An operation id is a hash of the actor, the tool and the idempotency key. The same triple always names the same operation. A second restart with that id does not increment the restart count.
