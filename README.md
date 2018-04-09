# Private Information Retrieval

This project is made by Nattapong Ekudomsuk

## How to run

### Directly

### Docker

Build this image using Docker. First, change the directory to django application root path. Now build the Docker image using this command

```docker build -t nutmos/pir:lastest .```

After the image build completed, using the command ```docker image ls``` will show the image. Run the image by using this command

```docker run -i -t -d -p 8000:8000 nutmos/pir:lastest```

Now the server running.
