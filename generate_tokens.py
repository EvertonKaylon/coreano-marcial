import json

with open("static/css/tokens/design_tokens.json") as f:
	tokens =json.load(f)

with open("static/css/design-tokens.css", "w") as css:
	css.write(":root {\n")
	
	for group, values in tokens.items():
		for key, value in values.items():
			css.write(f" --{group}-{key}: {value};\n")


	css.write("}\n")
