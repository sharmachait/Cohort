# redis replication
Leader-Follower architecture, (master replica)
replica instances are exact copies of the master instance
the replicas  reconnect to the master every time the connection is broken
the replica tries to be the exact copy of the master regardless of what happens to the master

## mechanism that keeps the instances in sync
1. When a master and a replica instance are well-connected, the master keeps the replica updated by sending a stream of commands to the replica to replicate the effects on the dataset
2. When the link between the master and the replica breaks, for network issues or because a timeout is sensed in the master or the replica, the replica reconnects and attempts to proceed with a partial resynchronization: it means that it will try to just obtain the part of the stream of commands it missed during the disconnection.
3. When a partial resynchronization is not possible, the replica will ask for a full resynchronization. the master makes a snapshot of all the data and send it to the replica, followed by the stream of commands after the snapshot

Redis replicas asynchronously acknowledge the amount of data they receive periodically with the master. So the master does not wait every time for a command to be processed by the replicas, however it knows, if needed, what replica already processed what command. This allows having optional synchronous replication.

Synchronous replication of certain data can be requested by the clients using the [`WAIT`](https://redis.io/commands/wait) command.

- Replicas are able to accept connections from other replicas. Aside from connecting a number of replicas to the same master, replicas can also be connected to other replicas in a cascading-like structure. Since Redis 4.0, all the sub-replicas will receive exactly the same replication stream from the master.

- Redis replication is non-blocking on the master side. This means that the master will continue to handle queries when one or more replicas perform the initial synchronization or a partial resynchronization.


### The `--replicaof` flag

By default, a Redis server assumes the "master" role. When the `--replicaof` flag is passed, the server assumes the "slave" role instead.

### TspListener and TcpClient in c#

##### TcpClient
```c#
var client = new TcpClient(hostIpAddress, portname);
NetworkStream stream = client.GetStream();
stream.Write(Encoding.UTF8.GetBytes("hello world"));
```

we can also use the connect method to connect to a tcp server/listener

it has three over loads

1. `Connect(IPEndPoint)`
	1. the IPEndpoint class is used to specify the full address of the host
2. `Connect(IPAddress, int32)`
	1. we can provide an instance of the IPAddress class with the port we want to connect to
3. `Connect(String, int32)`
	1. connects using the specified port and host

```c#
var client = new TcpClient();
client.Connect("192.168.1.161",9001);
```

##### Reading form the stream
using the StreamReader class
```c#
var reader = new StreamReader(stream,System.Text.Encoding.UTF8)
reader.ReadToEnd();
```

ReadToEnd function reads all the data that has been passed on the data stream
it blocks the tread till the connection is up

