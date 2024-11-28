extends RayCast3D

var current_interactable = null

signal interactable_hovered(intaractable)
signal interactable_unhovered()

func _process(delta):
	var collider = get_collider()
	if collider != current_interactable:
		if collider != null:
			# Attempt to find the Interactable node within the collider's children
			var interactable = collider.get_node_or_null("Interactable")
			if interactable != null:
				push_warning("qqqq")
				current_interactable = interactable
				interactable_hovered.emit(current_interactable)
			else:
				current_interactable = null
				interactable_unhovered.emit()
		else:
			current_interactable = null
			interactable_unhovered.emit()
			
func _input(event: InputEvent):
	if event is InputEventKey and event.is_action_pressed("interact"):
		if current_interactable != null:
			current_interactable.intaract()
		else:
			push_warning("TESTING")
