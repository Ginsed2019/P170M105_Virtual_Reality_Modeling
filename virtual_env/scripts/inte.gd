extends Node3D

class_name Inte

func inte():
	pass

func inte_verb():
	return "interact"

func get_color():
	for c in get_children():
		if c is MeshInstance3D:
			return c.get_active_material(0).albedo_color

func change_color(color):
	for c in get_children():
		if c is MeshInstance3D:
			c.get_active_material(0).albedo_color = color

func can_pickup():
	return true
