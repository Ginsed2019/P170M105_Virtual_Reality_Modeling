extends RayCast3D

var curr_inte = null

@export var pickup: Pickup

signal inte_hov(inte)
signal inte_unhov()

func _ready():
	self.collide_with_areas = true

func _process(delta: float):
	var collider = get_collider()
	if collider != curr_inte:
		if collider != null and collider is not Inte:
			curr_inte = null
			inte_unhov.emit()
		elif collider is Inte:
			push_warning(collider)
			curr_inte = collider
			inte_hov.emit(curr_inte)

func _input(event: InputEvent):
	if event is InputEventKey and event.is_action_pressed('inte'):
		if pickup.is_pickedup():
			pickup.rele_inte()
		else:
			if curr_inte != null:
				if (curr_inte is InteBallAdd or curr_inte is InteBox or curr_inte is InteSword) and curr_inte.can_pickup():
					pickup.pickup(curr_inte)
				else:
					curr_inte.inte()
