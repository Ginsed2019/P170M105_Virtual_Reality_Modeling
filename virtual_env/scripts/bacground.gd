extends WorldEnvironment

var time_passed = 0.0
var speed = 0.5

func _process(delta):
	time_passed += delta * speed

	var red = 0.5 + 0.5 * sin(time_passed)
	var green = 0.5 + 0.5 * sin(time_passed * 2 + 2.0)
	var blue = 0.5 + 0.5 * sin(time_passed * 3 + 4.0)

	var new_color = Color(red, green, blue)

	var env = environment
	if env:
		env.background_color = new_color
