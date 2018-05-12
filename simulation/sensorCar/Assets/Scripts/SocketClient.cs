using System.Collections;
using UnityEngine;
using SocketIO;

public class SocketClient : MonoBehaviour {

	private SocketIOComponent socket;

	public void Start()  {

		socket = GetComponent<SocketIOComponent>();

		socket.On("open", onOpen);
		socket.On("error", onError);
		socket.On("close", onClose);
		socket.On("receive", onSteer);
		
	}

	public void Update() {


	}

	public void onOpen(SocketIOEvent obj) {
		Debug.Log("[SocketIO] Open received: " + obj.name + " " + obj.data);
	}
	
	public void onError(SocketIOEvent obj) {
		Debug.Log("[SocketIO] Error received: " + obj.name + " " + obj.data);
	}
	
	public void onClose(SocketIOEvent obj) {	
		Debug.Log("[SocketIO] Close received: " + obj.name + " " + obj.data);
	}

	public void onSteer(SocketIOEvent obj) {
		Debug.Log("[SocketIO] Open received: " + obj.name + " " + obj.data);
		
		// TODO Steer car
	}
}
