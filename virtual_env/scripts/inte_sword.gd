extends Inte

class_name InteSword

func inte():
	pass

func inte_verb():
	return "pick up (Only affter touching white cube)"

func can_pickup():
	return get_color() == Color(1,1,1,1)
