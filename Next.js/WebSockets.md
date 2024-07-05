websockets in the backend are not supported, create an express app for that.
at the client side make sure the components are client side components if they try to connect to some web socket server.
```tsx
'use client'

import {useEffect,useState} from 'react';

export default function page(){
	const [socket,setSocket] = useState<WebSocket | null>(null);
	useEffect(()=>{
		const ws=new WebSocket('ws://localhost:8080');
		ws.onopen = ()=>{
			console.log("connection established");
			ws.send("hello from the client");
			setSocket(ws);
		}
		ws.onmessage = (message)=>{
			console.log(message);
		}
	return ()=>{ws.close();}
	});
	return (<div>hello</div>);
}
```