build:
	docker buildx build \
		-t jimyag/xiaomi-miio-exporter:latest \
		--push \
		--platform linux/amd64 .
