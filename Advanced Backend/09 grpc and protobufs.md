# protobufs
just a contract shared between the backend and the frontend
defines the shape of the data

message.proto
```protobuf
syntax="proto3";

message Person {
	string name = 1;
	int32 age = 2;
}
message GetPersonByNameRequest {
	string name = 1;
}
service PersonService {
	rpc AddPerson(Person) returns (Person);
	rpc GetPersonByName(GetPersonByNameRequest) returns (Person);
}
```

the one and two in the above example are known as field numbers they are used for backwards compatibility when we change the order of fields in our message as long as they have the same field number we will be backwards compatible
> npm i protobufjs

```js
const protobuf = require('protobufjs');

protobuf.load('a.proto')
	.then(root => {
		const Person = root.lookupType('Person');
		const person = {name:"somename", age:30};
		const buffer = Person.encode(person).finish();
		require('fs').writeFileSync('person.bin',buffer);
		console.log('Person serialized and saved to person.bin');
		const data =require('fs').readFileSync('person.bin');
		const deserializedPerson = Person.decode(data);
		console.log('Person deserialized from person.bin');
	})
	.catch(cnosole.error);
```

### protobuf data types

#### scalar
- int32, int64, uint32, uint64
- float, double
- bool
- string
- bytes
we can also have nested messages

```protobuf
message Address {
	string street = 1;
	string housenumber = 2;
}
message person {
	string name = 1;
	int32 age = 2;
	repeated string phoneNumber = 3;
	Address address = 4;
}
```
we can also have arrays of the types using the repeated keyword
#### message 
the message type allows us to define objects

#### enum
```protobuf
enum PhoneType {
	MOBILE = 0;
	LANDLINE = 1;
}
```
enum can be used in another message
while compressing we only need to give 0 or 1 the library will take care of replacing it with MOBILE or LANDLINE
#### maps
```protobuf
message MapName {
	map<string, int32> id_to_age = 1;
}
```

# grpc

> npm i @grpc/grpc-js @grpc/proto-loader

```ts
import path from 'path';
import * as grpc from '@grpc/grpc-js';
import {GrpcObject, ServiceClientConstructor} from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';

const package = protoLoader.loadSync(path.join(__dirname,'a.proto'));
const personProto = grpc.loadPackageDefinition(package);

const persons: Person[] = [];

function addPerson(call,callback){// req, res
	
	let person: Person = {
		name:call.request.name,
		age: call.request.age
	};
	persons.push(person);
	callback(null, person);// error, response
}
function getPersonByName(call,callback){
	const name = call.request.name;
	const person = persons.find(
		x => x.name === name
	);
	callback(null, person);
}

const server = grpc.Server();

server.addService(
	(personProto.PersonService as ServiceClientConstructor).service
	, { 
		AddPerson : addPerson
		, GetPersonByName : getPersonByName
	 }
);

server.bindAsync(
	'0.0.0.0:50051'
	, grpc.ServerCredentials.createInsecure()
	, ()=>{ server.start(); }
);

```

but what will the route for the addPerson function look like ?

grpc://localhost:50051 PersonService AddPerson

we can auto complete for this on postman we just need to upload our proto file to it

we can generate the typescirpt types from the proto file using the proto-loader-gen-types script

> node node_modules/@grpc/proto-loader/build/bin/proto-loader-gen-types.js