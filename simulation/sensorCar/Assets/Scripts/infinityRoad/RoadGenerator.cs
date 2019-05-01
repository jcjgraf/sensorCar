using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RoadGenerator : MonoBehaviour {

	public Transform car;

	public int numberOfSegments = 7;

	public bool removePassedSegments = true;

	public RoadSegment[] roadSegments;

	private Vector3 segmentStartPosition;
	private Vector3 segmentStartRotation;

	private Queue<Transform> roadSegmentsQueue;

	private GameObject lastRoadSegment;

	private int lastIndex;

	private List<Vector3> startPositionList;
	private List<Vector3> startRotationList;

	//TODO for debugging
	private List<int> numberList;

	// Needed since it might trigger several collisions in the same frame
	private bool hasTriggered = false;

	void Awake() {

		TriggerManager.colliderTriggered += trigger;

		roadSegmentsQueue = new Queue<Transform>();
		segmentStartPosition = new Vector3(0, 0, 0);
		segmentStartRotation = new Vector3(0, 0, 0);

		startPositionList = new List<Vector3>();
		startRotationList = new List<Vector3>();
		startPositionList.Add(segmentStartPosition);
		startRotationList.Add(segmentStartRotation);

		lastIndex = 0;

		//TODO for debugging
		numberList = new List<int>() { 0, 0, 1, 1, 2, 2, 0, 1, 0, 0, 1, 1, 0, 2, 1, 0, 2, 2, 0, 0, 1, 1, 0, 0, 0, 1, 2, 1, 2, 0, 0, 1, 1, 0, 2, 0, 0, 0 };

		// Create straight road segments at the beginning
		generateRoad(0);
	}
	
	void Update() {
		/*
			Get the name resp. its number of the first segment in the roadSegmentsQueme and compare it the with segment the car is on currently. If it has passed the first segment, destroy it and generate a new one.
		*/

		int firstSegment;
		int.TryParse(roadSegmentsQueue.ToArray()[0].gameObject.GetComponentInChildren<Transform>().GetChild(0).name, out firstSegment);

		if (getCurrentSegment() > firstSegment + 1) { // + 1 in order to always leave a segment

			Transform toRemove = roadSegmentsQueue.Dequeue();

			if (removePassedSegments) {
				Destroy (toRemove.gameObject);

				startPositionList.RemoveAt (0);
				startRotationList.RemoveAt (0);
			}
		}

		generateRoad();

		hasTriggered = false;
	}

	int getCurrentSegment() {
		/*	
			Use a raycast in order at the center of the car in order to find out the object which the car is currently on.	
		*/

		RaycastHit hit;

		Vector3 rayUnitVector = new Vector3(0, -1, 0);

		if (Physics.Raycast(car.position, rayUnitVector, out hit, Mathf.Infinity)) {

			Debug.DrawLine(car.position, hit.point, Color.red);

			int colliderName;
			int.TryParse(hit.collider.name, out colliderName);

			return colliderName;
		}

		return 0;
	}

	void generateRoad() {

		if (roadSegmentsQueue.ToArray().Length == numberOfSegments) {
			return;
		}

		addSegment();
		generateRoad();
	}

	void generateRoad(int segmentInt) {

		if (roadSegmentsQueue.Count == numberOfSegments) {
			return;
		}

		addSegment(segmentInt);
		generateRoad(segmentInt);
	}

	void addSegment() {

		addSegment(Random.Range(0, roadSegments.Length));
	}

	void addSegment(int segmentInt) {

		RoadSegment newRoadSegment;

		if (segmentInt > roadSegments.Length) {
			// Ugly way to generate more straight segments
			newRoadSegment = roadSegments[0];

		} else {
			newRoadSegment = roadSegments[segmentInt];
		}

		//TODO uncomment for debugging
//		newRoadSegment = roadSegments[numberList[0]];
//		numberList.RemoveAt(0);

		GameObject newSegment = Instantiate<GameObject>(newRoadSegment.prefab);

		// Start - used for detecting collisions
		// Setup Rigidbody
		Rigidbody newSegementRigidbody =  newSegment.AddComponent<Rigidbody>();
		newSegementRigidbody.isKinematic = true;

		// Add the class with the triggerEvent to the newly created gameObject
		newSegment.AddComponent(typeof(TriggerManager));

		// Add collider and set right properties
		MeshCollider newSegmentCollider = newSegment.gameObject.GetComponentInChildren<Transform>().GetChild(0).GetComponent<MeshCollider>();

		newSegmentCollider.convex = true;
		newSegmentCollider.isTrigger = true;
		// End - used for detecting collisions

		// Transform new gameObject
		newSegment.transform.position = segmentStartPosition + newRoadSegment.standardPosition;
		newSegment.transform.eulerAngles = segmentStartRotation + newRoadSegment.standardRotation;
		newSegment.transform.localScale = newRoadSegment.standardScale;

		// Set name of the road Segment
		newSegment.gameObject.GetComponentInChildren<Transform>().GetChild(0).name = lastIndex.ToString();

		lastIndex++;

		// Update position and rotation
		// Deg to Rad
		float angle = -1 * (segmentStartRotation.y * Mathf.PI / 180);  // The -1 is needed since the rotation matrix works in the other way around as the unity rotation system
		// Apply a rotation vectory
		// Multiply by the roation matrix
		Vector3 deltaMove = new Vector3(newRoadSegment.deltaEndPosition.x * Mathf.Cos(angle) - newRoadSegment.deltaEndPosition.z * Mathf.Sin(angle), 0, newRoadSegment.deltaEndPosition.x * Mathf.Sin(angle) + newRoadSegment.deltaEndPosition.z * Mathf.Cos(angle));
	
		segmentStartPosition = segmentStartPosition + deltaMove;
		segmentStartRotation = segmentStartRotation + newRoadSegment.deltaEndRotation;

		startPositionList.Add (segmentStartPosition);
		startRotationList.Add (segmentStartRotation);

		roadSegmentsQueue.Enqueue(newSegment.transform);

		// remove trigger detection thingis of the second last road segment since there is already a new one in place on the new last one
		try {
			removeTriggerDetection(lastRoadSegment);
		}
		catch {}

		lastRoadSegment = newSegment;
	}

	void removeTriggerDetection(GameObject segment) {

		// Undo changes
		segment.gameObject.GetComponentInChildren<Transform>().GetChild(0).GetComponent<MeshCollider>().isTrigger = false;
		segment.gameObject.GetComponentInChildren<Transform>().GetChild(0).GetComponent<MeshCollider>().convex = false;
		Destroy(segment.GetComponent<TriggerManager>());

	}

	void trigger(Collider collider) {

		int colliderNameInt = 0;
		int segmentNameInt = 0;

		bool parseI = int.TryParse (collider.gameObject.name, out colliderNameInt);
		bool parseII = int.TryParse (lastRoadSegment.GetComponentInChildren<Transform> ().GetChild (0).name, out segmentNameInt);

		// If both parse succeedes, i.e. both are road segments
		if (parseI && parseII && hasTriggered == false) {

			// Collision with previous road segment (or with own segment for some reason) are legal
			if (colliderNameInt + 1 == segmentNameInt || colliderNameInt == segmentNameInt) {
				 Debug.Log("Legal collision");

			// Collision with another road segment
			} else {
				Debug.Log ("Collided with " + collider.gameObject.name + " - " + lastRoadSegment.GetComponentInChildren<Transform> ().GetChild (0).name);

				// One collision might be triggered several times. After removing it after the first collision a it cannot be removed a second time -> an err is thorwn
				try {

					// Since it is not possible to remove from the end of a queue with have to go through the list until we are at the elements of the end which we want to remove
					for (int j = 0; j < numberOfSegments; j++) {

						// This - n is the number of segments which we want to remove after a collision was detected
						if (j < numberOfSegments - 2) {
							Debug.Log("Add segment to the end");
							roadSegmentsQueue.Enqueue(roadSegmentsQueue.Dequeue());

						} else {
							Debug.Log("Destroy segment");

							Transform segment = roadSegmentsQueue.Dequeue();

							startPositionList.RemoveAt(startPositionList.Count - 1);
							startRotationList.RemoveAt(startRotationList.Count - 1);

							segmentStartPosition = startPositionList[startPositionList.Count - 1];
							segmentStartRotation = startRotationList[startRotationList.Count - 1];

							hasTriggered = true;	
							Destroy (segment.gameObject);

							lastIndex--;
						}
					}
				} catch {
					Debug.Log ("Element already removed");
				}
			}
		}
	}
}
