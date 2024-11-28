extends Inte

class_name InteBox

func _on_body_entered(body: Node3D) -> void:
	if body is InteBallAdd:
		var color = body.color
		for c in get_children():
			if c is MeshInstance3D:
				c.get_active_material(0).albedo_color += color
		body.queue_free()
	if body is InteSword:
		if get_color() == Color(1, 1, 1, 4):
			body.change_color(Color(1, 1, 1))
			queue_free()

func inte():
	pass

func inte_verb():
	return "pick up"
