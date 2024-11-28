extends Inte

var is_killed = false
var created = 0

@export var script_path: String = "res://scripts/inte_ball_add.gd"

func _on_area_3d_body_entered(body: Node3D) -> void:
	if body is InteSword:
		body.queue_free()
		is_killed = true
		change_color(Color(1, 1, 1))
		var area = $Area3D
		if area:
			area.queue_free()

func inte_verb():
	return "extract cube"

func inte():
	if not is_killed:
		return  # Only works on "killed" cubes
	if (created == 0):
		create_small_cube(Color(1,1,1))
	elif (created == 1):
		create_small_cube(Color(1,0,0))
		change_color(Color(0,1,1))
	elif (created == 2):
		create_small_cube(Color(0,1,0))
		change_color(Color(0,0,1))
	elif (created == 3):
		create_small_cube(Color(0,0,1))
		change_color(Color(0,0,0))
	elif (created == 4):
		create_small_cube(Color(0,0,0))
		queue_free()
	created += 1
		

func create_small_cube(color):
	var small_cube = RigidBody3D.new()

	var mesh_instance = MeshInstance3D.new()
	var box_mesh = BoxMesh.new()
	box_mesh.size = Vector3(0.3, 0.3, 0.3)
	mesh_instance.mesh = box_mesh
	
	var material = StandardMaterial3D.new()
	material.albedo_color = color
	mesh_instance.material_override = material
	small_cube.add_child(mesh_instance)

	var collision_shape = CollisionShape3D.new()
	var box_shape = BoxShape3D.new()
	box_shape.extents = Vector3(0.15, 0.15, 0.15)
	collision_shape.shape = box_shape
	small_cube.add_child(collision_shape)

	small_cube.transform.origin = self.transform.origin + Vector3(randf() - 0.5, randf() - 0.5, randf() - 0.5)

	var script = load(script_path)
	small_cube.set_script(script)

	get_tree().root.add_child(small_cube)
