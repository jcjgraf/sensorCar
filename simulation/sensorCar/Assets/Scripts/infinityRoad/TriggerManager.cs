using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TriggerManager : MonoBehaviour {

	public delegate void TriggerEvent(Collider collider);
	public static event TriggerEvent colliderTriggered;

	void OnTriggerEnter(Collider collider) {

		if (collider.gameObject.name != "Plane") {

			// Debug.Log("Intersecting roads detected: " + collider.gameObject.name);
			
			// make sure that we have a subscriber before calling the event
			if (colliderTriggered != null) {
				colliderTriggered(collider);
			}

		}
    }
}
