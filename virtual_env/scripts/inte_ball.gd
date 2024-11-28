extends Inte

func inte():
	for c in get_children():
		if c is MeshInstance3D:
			var val = c.get_active_material(0).albedo_color[0] + 0.1
			if val > 1: val = 0
			c.get_active_material(0).albedo_color = Color(val, 0, 0)

func inte_verb():
	return "change color"
	
# 25min+
