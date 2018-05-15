using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIO;

public class SocketClient : MonoBehaviour {

	private SocketIOComponent socket;
	
	private bool doRecord = false;

	Dictionary<string, string> data;


	public void Start()  {

		socket = GetComponent<SocketIOComponent>();

		socket.On("open", onOpen);
		socket.On("error", onError);
		socket.On("close", onClose);
		socket.On("steer", onSteer);
		
	}

	public void Update() {

		if (doRecord) {
			doRecord = false;

			// TODO collect data

			Debug.Log("Recording data");

			data = new Dictionary<string, string>();

			data["s1"] = "1.23";
			data["s2"] = "2.54";
			data["s3"] = "12.33";

			Debug.Log("Emitting data");

			socket.Emit("evaluate", new JSONObject(data));

			Debug.Log("Emitted data");
		}

	}

	public void onOpen(SocketIOEvent obj) {
		Debug.Log("[SocketIO] Open received: " + obj.name + " " + obj.data);

		doRecord = true;
	}
	
	public void onError(SocketIOEvent obj) {
		Debug.Log("[SocketIO] Error received: " + obj.name + " " + obj.data);

		doRecord = false;
	}
	
	public void onClose(SocketIOEvent obj) {	
		Debug.Log("[SocketIO] Close received: " + obj.name + " " + obj.data);

		doRecord = false;
	}

	public void onSteer(SocketIOEvent obj) {
		Debug.Log("rec");
		Debug.Log("[SocketIO] Steer received: " + obj.name + " " + obj.data);
		
		// TODO Steer car

		doRecord = true;
	}
}
