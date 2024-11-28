extends Inte

class_name InteBallAdd

@export var color = Color(1, 0, 0)

func _ready():
	for c in get_children():
		if c is MeshInstance3D:
			var material = c.get_active_material(0).duplicate()
			material.albedo_color = color
			c.set_surface_override_material(0, material)

func inte():
	pass

func inte_verb():
	return "pick up"
	
# 25min+
