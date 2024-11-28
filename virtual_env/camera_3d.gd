extends Camera3D

var speed = 5  # Movement speed
var rotation_speed = 2  # Rotation speed

func _process(delta):
	var input_dir = Vector3()

	# Movement inputs
	if Input.is_action_pressed("move_forward"):
		input_dir += -global_transform.basis.z
	if Input.is_action_pressed("move_backward"):
		input_dir += global_transform.basis.z
	if Input.is_action_pressed("move_left"):
		input_dir += -global_transform.basis.x
	if Input.is_action_pressed("move_right"):
		input_dir += global_transform.basis.x
	if Input.is_action_pressed("move_up"):  # R key
		input_dir += global_transform.basis.y
	if Input.is_action_pressed("move_down"):  # T key
		input_dir += -global_transform.basis.y

	# Normalize and apply movement
	if input_dir != Vector3.ZERO:
		input_dir = input_dir.normalized()
		global_translate(input_dir * speed * delta)

	# Rotation inputs
	if Input.is_action_pressed("rotate_left"):  # Q key
		rotate_y(-rotation_speed * delta)
	if Input.is_action_pressed("rotate_right"):  # E key
		rotate_y(rotation_speed * delta)
