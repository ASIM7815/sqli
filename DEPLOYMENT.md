# QueryQuest deployment guide (organizer only)

This package runs the deliberately vulnerable QueryQuest application in
its own Docker container. It is intended for a controlled CTF challenge
instance, not for general-purpose hosting.

## 1. Requirements

- A Linux VPS/server with Docker Engine and Docker Compose plugin.
- A DNS hostname pointing to the server.
- HTTPS reverse proxy (for example, Nginx or Caddy) in front of the app.
- Firewall access limited to the reverse proxy and administrator SSH.
- A unique flag and a strong Flask session secret.

## 2. Configure secrets

From this directory:

```bash
cp .env.example .env
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

Edit `.env` and set:
- `CTF_FLAG` to a unique flag for this challenge (do not reuse a flag from another challenge).
- `SECRET_KEY` to the generated random value.

Keep `.env` private. Do not upload it to a public website/repository,
include it in participant downloads, or paste it into public logs.

Example format only:

```dotenv
CTF_FLAG=CTF{your_unique_random_value}
SECRET_KEY=paste_a_generated_64_character_hex_secret_here
```

## 3. Build and start

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f queryquest
```

The app is bound to `127.0.0.1:5002` on the server, not directly to every
network interface. The database is initialized automatically on first
startup and stored in the named Docker volume `queryquest-data`.

Test locally on the server:

```bash
curl -I http://127.0.0.1:5002/login
```

A redirect or HTTP 200 response is expected; the login page should load.

## 4. Put HTTPS in front

Configure your existing Nginx/Caddy reverse proxy for your challenge
hostname and proxy requests to:

```text
http://127.0.0.1:5002
```

Enable a valid TLS certificate. Preserve the original Host and forwarded
protocol headers. Since `COOKIE_SECURE=1` is set in Compose, serve the
challenge over HTTPS; browser sessions may not work over plain HTTP.

Do not expose port 5002 publicly. Keep only SSH and HTTPS open in the
server firewall (plus any separately required CTF platform ports).

## 5. Add it to your CTF website (for example, CTFd)

Create a challenge entry in your CTF platform:

- **Name:** QueryQuest — The Forgotten Records
- **Category:** Web Exploitation
- **Value:** 300–350 points (suggested)
- **Type:** Standard / static flag
- **Connection info:** `https://YOUR-CHALLENGE-HOSTNAME`
- **Description:** Use the participant description in `PARTICIPANT_CHALLENGE.md`.
- **Flag:** Set the exact same value as `CTF_FLAG` in the server's private `.env`.
- **Hints:** Release progressively if your platform supports hints.

Participants should open the challenge URL in a new tab. The ZIP itself is
an organizer deployment package; normally you do not give this ZIP to
participants. If your CTF platform has a challenge attachment feature,
only upload participant-safe files, never this deployment package or `.env`.

## 6. Verify before the event

1. Open the public HTTPS URL in a private/incognito browser.
2. Confirm the login page loads and HTTPS is valid.
3. Log in with `trainee` / `trainee123`.
4. Confirm dashboard, records, and search pages load.
5. Confirm the challenge is reachable from a participant network.
6. Solve the challenge from a clean browser/account using your private organizer notes.
7. Submit the exact configured flag to the CTF platform and confirm acceptance.
8. Confirm that no database, `.env`, source-control, or debug endpoints are exposed.

## 7. Operations and backups

View logs:

```bash
docker compose logs --tail=200 queryquest
```

Restart:

```bash
docker compose restart queryquest
```

Stop:

```bash
docker compose down
```

The database persists in the `queryquest-data` volume when the container is
recreated. Back it up before upgrades:

```bash
docker compose stop queryquest
docker run --rm -v queryquest-data:/data -v "$PWD":/backup \
  alpine sh -c 'cd /data && tar czf /backup/queryquest-db-backup.tgz .'
docker compose start queryquest
```

Do not use `docker compose down -v` unless you intentionally want to delete
the persistent database volume and all challenge state.

## 8. Security isolation

This app contains an intentional SQL injection vulnerability. Run it in a
dedicated container/VM, separate from CTFd, databases, admin panels, and
other sensitive services. Do not mount host directories or Docker sockets
into the container. Do not reuse production credentials. Apply host firewall
rules, keep Docker and the OS patched, monitor logs, and destroy the
challenge instance after the event.

The login credentials are shared by all participants by design. The
challenge database is local to this app. Do not put real personal,
corporate, or production data in it.

## 9. Troubleshooting

**Container does not start:**
```bash
docker compose logs --tail=200 queryquest
```

**Port 5002 is occupied:** change the left side of the Compose port mapping,
for example `127.0.0.1:5012:5000`, and update your reverse proxy upstream.

**Need to rebuild app code:**
```bash
docker compose down
docker compose up -d --build
```

**Need to reinitialize the database:** this deletes challenge progress and
recreates the database. Back it up first, then remove only the named volume
after stopping the service:
```bash
docker compose down
docker volume ls
# Identify the project-prefixed queryquest-data volume, then remove it:
docker volume rm YOUR_PROJECT_QUERYQUEST_DATA_VOLUME
docker compose up -d
```

Never run destructive reset commands on the live event instance without
an explicit backup and organizer approval.
