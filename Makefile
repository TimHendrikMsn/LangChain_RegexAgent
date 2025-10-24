IMAGE_NAME=lc-tsc-image
CONTAINER_NAME=lc-tsc-container


build:
	docker build -t $(IMAGE_NAME) -f Dockerfile .

build-no-cache:
	docker build --no-cache -t $(IMAGE_NAME) -f Dockerfile .

terminal:
	docker run -it --rm \
		--env-file .env \
		-v "$(PWD)/src":/app \
		--workdir /app \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME) /bin/sh