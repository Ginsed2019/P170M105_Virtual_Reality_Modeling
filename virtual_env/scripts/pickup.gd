extends Node3D

class_name Pickup

var cure_pickup_inte = null;

func pickup(inte):
	if cure_pickup_inte != null:
		rele_inte()
	else:
		pickup_inte(inte)

func rele_inte():
	remove_child(cure_pickup_inte)
	get_parent().get_parent().get_parent().add_child(cure_pickup_inte)
	cure_pickup_inte.global_transform.origin = global_transform.origin
	if cure_pickup_inte is RigidBody3D:
		cure_pickup_inte.freeze = false
	for c in cure_pickup_inte.get_children():
		if c is CollisionShape3D:
			c.disabled = false
	cure_pickup_inte = null

func pickup_inte(inte):
	cure_pickup_inte = inte
	cure_pickup_inte.get_parent().remove_child(cure_pickup_inte)
	add_child(cure_pickup_inte)
	cure_pickup_inte.global_transform.origin = global_transform.origin
	if cure_pickup_inte is RigidBody3D:
		cure_pickup_inte.freeze = true
	for c in cure_pickup_inte.get_children():
		if c is CollisionShape3D:
			c.disabled = true

func is_pickedup():
	return cure_pickup_inte != null
