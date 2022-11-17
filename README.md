
A local productivity and organisational tool for me and my needs. Also, a general playground for coding and web development tools, which is why it's filled with woefully out-of-place and overengineered solutions.

## Running Diary

```bash
# Test dev

# Test prod


# Run dev
docker-compose --file=docker-compose.yml --env-file=.env.local up

# Run prod
docker-compose --file=docker-compose.prod.yml --env-file=.env.production up -d

```