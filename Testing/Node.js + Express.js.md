# jest
> npm install --save-dev ts-jest @jest/globals
> npx ts-jest config:init

this creates the jest.config.js

package.json
```json
"scripts":{
	"test":"jest"
}
```

create tests/index.test.ts
```ts
import {describe, expect, test} from "@jest/globals";
import {functionToTest} from '../index';

describe("some function", ()=>{
	test("adds 1 and 2 to equal 3", ()=>{
		expect(functionToTest(1,2)).toBe(3);
	});
});
```

jest goes through the complete source code, each and every file and execute all files that end with .test.ts

describe functions are used for different units of code that we want to test

instead of the test function we can also use the it function

```ts
import {describe, expect, it} from "@jest/globals";
import {functionToTest} from '../index';

describe("some function", ()=>{
	it("adds 1 and 2 to equal 3", ()=>{
		expect(functionToTest(1,2)).toBe(3);
	});
});
```

we can next the describe functions
it will just do logging better when running the tests to understand the scope of the units being tested better

# supertest
used to test api backend for express

>npm i supertest @types/supertest

in the express code base we will need to export the app instance and we dont need to actuall start the express server with app.listen()

```ts
import express from "express";

export const app = express();

app.use(express.json());

app.post("/sum", (req,res)=>{
	const a = req.body.a;
	const b = req.body.b;
	res.json({
		answer: a+b;
	});
});
```

but then how will my code actually work? 
in a different file called maybe bin.ts or server.ts
import app from ./index and do app.listen in that file

so to run the application we can run the dist/bin.js file instead

```ts
import {dscribe, expect, it} from "@jest/globals";
import request from "supertest";
import {app} from "../index";

describe("POST /sum",()=>{
	it ("should return the sum of two number", async () =>{
		const res = await request(app).post("/sum").send({
			a:1,
			b:2
		});
		expect(res.statusCode).toBe(200);
		expect(req.body.answer).tobe(3);
	})
})
```

how to make it actually work when the endpoint is connecting to a database? we mock the data
