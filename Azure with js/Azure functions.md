when we crate an azure function app we can define many functions under the azure function app

a storage account is needed to store the function code and configuration files
but only if the plan we chose is consumption or premium

we can also use existing app service plans

function apps can also have application insights associated with them for monitoring and logging

### disadvantages
1. vendor lock in
2. cold start - less for interpreted languages
3. resource limits, functions can not run for more than 10 minutes and can not take more than some amount of limited memory.

to make the function acccessible publicly we have to change the trigger authorization level to be anonymous in the intergration section of the individual function
# refactoring express.js to azure functions

1. ensure middleware logic is taken care of
2. The api used to process requests and responses differ
3. az func endpoints are exposed under api route
4. routing rules can be configured via routePrefix in the host,json file
5. function.json file to define HTTP verbs, define security policies, and can configure the function's input and output
6. By default, the folder name that which contains the function files defines the endpoint name, but you can change the name via the route property in the function.json file.

```js
// server.js
app.get('/hello', (req, res) => {
  try {
    res.send("Success!");
  } catch(error) {
    const err = JSON.stringify(error);
    res.status(500).send(`Request error. ${err}`);
  }
});
```

a function named hello has a folder with the following files.

- hello
    - function.json
    - index.js

```ts
import { AzureFunction, Context, HttpRequest } from "@azure/functions";

const httpTrigger: AzureFunction = async function (context: Context, req: HttpRequest): Promise<void> {
  try {
    context.res = { body: "Success!" };
  } catch (error) {
    const err = JSON.stringify(error);
    context.res = {
      status: 500,
      body: `Request error. ${err}`,
    };
  }
};

export default httpTrigger;
```

- define the HTTP verbs in the function.json file such as POST or PUT.

```json
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get","post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
```

example, migrating express code to azure functions

```js
import * as express from 'express';
import { vacationService } from '../services';

const router = express.Router();

router.get('/vacations', (req, res) => {    // API route
  vacationService.getVacations(req, res);   // Data access logic
});
```

translates to

```ts
import { app } from '@azure/functions';
import { HttpRequest, HttpResponseInit, InvocationContext } from '@azure/functions';
import * as vacationService from '../services';

export async function getVacations(request, context) {
    return {
        status: 200,
        jsonBody: vacationService.getVacations(); // Data access logic
    };
};

app.http('get-vacations', {  // API route
    methods: ['GET'],
    route: 'vacations',
    authLevel: 'anonymous',
    handler: getVacations
});
```

change the route endpoint for a function in a folder named _getVacations_ to `vacations`
the `route` is way to set the function's route.

## env variables like connection string to the database
in the configuration tab in the LHS menu
for node.js use application settings
if in .net we can also use the connection strings in the configuration tab
add the variable in the application settings, but how to use it in the code?
just like you would for any other env variable via `process.env.variabelName`

![[Pasted image 20240706122555.png]]
