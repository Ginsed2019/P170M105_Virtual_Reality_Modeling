extends DirectionalLight3D

@export var center_position: Vector3 = Vector3.ZERO
@export var rotation_speed: float = 30.0  # Degrees per second
@export var rotation_radius: float = 5.0  # Distance from the center

var current_angle: float = 0.0

func _ready():
	position = center_position + Vector3(rotation_radius, position.y, 0)

func _process(delta):
	current_angle += rotation_speed * delta
	if current_angle >= 360.0:
		current_angle -= 360.0

	var x = rotation_radius * cos(deg_to_rad(current_angle))
	var z = rotation_radius * sin(deg_to_rad(current_angle))
	position = center_position + Vector3(x, position.y, z)

	look_at(center_position)
