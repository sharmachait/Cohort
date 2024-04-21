The 'Service' that sends an email-verification email to the person who has just registered must not halt the flow of the main website, and its fine, rather desirable that sending email is handled by a service not coupled with the service that wants to send the email.
It should be a microservice on its own.

using Azure service bus queues to achieve that

our registration backend endpoint will publish a message to azure queue and tell the user that an email has been sent, and its fine if the email takes a minute or two to be sent by the email service.

the email service will subscribe to the azure service bus queue, read messages and send the emails.

### topics vs queues
use queues when we only want one consumer to the published messages
but if want multiple subscribers use topics

since we only want one publisher, the service that handles all the registrations and only one consumer the service that send emails, we can use a simple queue

this is what the code to send messages should look like

```js
const { ServiceBusClient } = require('@azure/service-bus');  
const { v4: uuidv4 } = require('uuid');  
  
async function PublishMessage(message) {  
  try {  
    let messageBusClient = new ServiceBusClient(  
      process.env.SERVICEBUSCONNECTIONSTRING  
    );  
    let sender = messageBusClient.createSender(process.env.QUEUENAME);  
  
    const serviceBusMessage = {  
      body: message,  
      correlationId: uuidv4(),  
    };  
    await sender.sendMessages(serviceBusMessage);  
    await messageBusClient.close();  
  } catch (e) {  
    console.log(e);  
  }  
}  
  
module.exports = PublishMessage;
```

this is what the code to receive messages should look like

```js
const { isServiceBusError, ServiceBusClient } = require('@azure/service-bus');  
  
const sendMail = require('./emailService');  
  
const dotenv = require('dotenv');  
dotenv.config();  
  
async function processMessage(message) {  
  console.log({ message });  
  console.log(typeof message);  
  console.log(message.body);  
}  
  
async function processError(args) {  
  console.log(`Error from source ${args.errorSource} occurred: `, args.error);  
  if (isServiceBusError(args.error)) {  
    switch (args.error.code) {  
      case 'MessagingEntityDisabled':  
      case 'MessagingEntityNotFound':  
      case 'UnauthorizedAccess':  
        console.log(  
          `An unrecoverable error occurred. Stopping processing. ${args.error.code}`,  
          args.error  
        );  
        await subscription.close();  
        break;  
      case 'MessageLockLost':  
        console.log(`Message lock lost for message`, args.error);  
        break;  
      case 'ServiceBusy':  
        await delay(1000);  
        break;  
    }  
  }}  
  
async function readFromQueue() {  
  let messageBusClient = new ServiceBusClient(  
    process.env.SERVICEBUSCONNECTIONSTRING  
  );  
  let receiver = messageBusClient.createReceiver(process.env.QUEUENAME);  
  try {  
    const subscription = receiver.subscribe({  
      processMessage,  
      processError,  
    });  
  } catch (e) {  
    console.log(e);  
    await messageBusClient.close();  
  }  
}  
  
readFromQueue().catch((err) => {  
  console.log('ReceiveMessagesStreaming - Error occurred: ', err);  
  process.exit(1);  
});
```

change the processMessage function as per your requirements

![[Pasted image 20240420221146.png]]