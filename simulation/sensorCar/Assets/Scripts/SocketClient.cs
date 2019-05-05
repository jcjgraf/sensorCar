using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIO;
using UnityStandardAssets.CrossPlatformInput;

namespace UnityStandardAssets.Vehicles.Car {

	[RequireComponent(typeof (CarController))]
	public class SocketClient : MonoBehaviour {

		private CarController carController;
		private SocketIOComponent socket;
		private CarSensor carSensor;
		
		private bool doRecord = false;

		private bool netControl = false;

		Dictionary<string, string> data;

		[SerializeField] private bool doNetSteer = true;

		[SerializeField] private float verticalInput = 0.25f;
		[SerializeField] private bool doAutoAccelerate = false;
		[SerializeField] private bool doIgnoreVertical = false;

		public void Start()  {

			carController = GetComponent<CarController>();
			socket = GetComponent<SocketIOComponent>();
			carSensor = GetComponent<CarSensor>();

			socket.On("open", onOpen);
			socket.On("error", onError);
			socket.On("close", onClose);
			socket.On("steer", onSteer);		
		}

		public void Update() {

			if (!doNetSteer || netControl == false) {
				float h = CrossPlatformInputManager.GetAxis ("Horizontal");
				float v = CrossPlatformInputManager.GetAxis ("Vertical");
				float handbrake = CrossPlatformInputManager.GetAxis ("Jump");

				carController.Move (h, v, v, handbrake);


			} else if (netControl && CrossPlatformInputManager.GetAxis ("Horizontal") != 0) {

				float h = CrossPlatformInputManager.GetAxis ("Horizontal");
				float v = 0f;

				if (doAutoAccelerate) {
					v = verticalInput;
				
				} else if (doIgnoreVertical == false) {
					v = CrossPlatformInputManager.GetAxis ("Vertical");
				}

				float handbrake = CrossPlatformInputManager.GetAxis ("Jump");
				carController.Move (h, v, v, handbrake);

			} else if (netControl && doRecord) {

				doRecord = false;

				// collect data
				data = new Dictionary<string, string> ();

				for (int i = 0; i < carSensor.distances.Count; i++) {

					if (float.IsInfinity (carSensor.distances [i])) {
						doRecord = true;
						return;

					} else {
						data ["s" + i.ToString ()] = carSensor.distances [i].ToString ();
					}
				}

				Debug.Log (new JSONObject (data));

				socket.Emit ("evaluate", new JSONObject (data));
			}

		}

		public void onOpen(SocketIOEvent obj) {
			Debug.Log("[SocketIO] Open received: " + obj.name + " " + obj.data);

			doRecord = true;
			netControl = true;
		}
		
		public void onError(SocketIOEvent obj) {
//			Debug.Log("[SocketIO] Error received: " + obj.name + " " + obj.data);

			doRecord = false;
			netControl = false;
		}
		
		public void onClose(SocketIOEvent obj) {	
			Debug.Log("[SocketIO] Close received: " + obj.name + " " + obj.data);

			doRecord = false;
			netControl = false;
		}

		public void onSteer(SocketIOEvent obj) {
			Debug.Log("[SocketIO] Steer received: " + obj.name + " " + obj.data);

			// Retrieve json and converte to 
			JSONObject jsonData = obj.data;
			string jsonString = jsonData.GetField("steering_angle").str;
			float steering = float.Parse(jsonString);

			Debug.Log("Steering Angle: " + steering);

			float v = 0f;

			if (doAutoAccelerate) {
				v = verticalInput;

			} else if (doIgnoreVertical == false) {
				v = CrossPlatformInputManager.GetAxis ("Vertical");
			}

			carController.netMove(steering, v, v, 0.0f);

			doRecord = true;
		}
	}
}
