pretty_path1 = ./src/**/**.js
pretty_path2 = ./src/**.js


server:
	python manage.py runsslserver 8000 --key localhost.key --certificate localhost.crt

prettier:
	prettier ${pretty_path1} --write
