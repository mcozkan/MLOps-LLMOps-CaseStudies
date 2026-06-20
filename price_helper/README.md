# Week-10 Homework: Gitea Actions CI/CD Pipeline

This repository contains a small Python pricing helper application and a multi-job Gitea Actions CI/CD pipeline.

## What the app does

The app has one importable function:

```python
calculate_discounted_price(price: float, discount_percent: float) -> float
```

It calculates the final product price after applying a percentage discount.

Example:

```python
calculate_discounted_price(100, 15)
# 85.0
```

Invalid inputs raise clear exceptions. For example, a discount below `0` or above `100` raises `ValueError`.

## Project structure

```text
.
├── .gitea/
│   └── workflows/
│       └── ci.yaml
├── tests/
│   └── test_app.py
├── app.py
├── main.py
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

Expected output:

```text
Original price: 250.0
Discount: 20.0%
Final price: 200.0
```

Run lint:

```bash
ruff check .
```

Run tests:

```bash
pytest -q
```

Build and run Docker image locally:

```bash
docker build -t price-helper:local .
docker run --rm price-helper:local
```

## Gitea Actions pipeline

The workflow is located at:

```text
.gitea/workflows/ci.yaml
```

It runs on every push and has three jobs:

1. `lint`
   - Runs `ruff check .`
   - Fails if lint errors exist

2. `test`
   - Runs `pytest -q`
   - Fails if tests fail

3. `build-and-push`
   - Depends on both `lint` and `test` using `needs:`
   - Always builds the Docker image on every branch
   - Runs a smoke test with `docker run`
   - Only on `main`, logs in to the local Gitea registry and pushes:
     - `:latest`
     - `:<short-sha>`

The short SHA is computed inside the workflow from `${{ github.sha }}`:

```bash
SHORT_SHA=$(echo "${{ github.sha }}" | cut -c1-7)
```

## Required Gitea secret

Create a Gitea Personal Access Token with `write:package` permission.

Then add it to the repository:

```text
Repo → Settings → Actions → Secrets → Add Secret
```

Secret name:

```text
GITEATOKEN
```

The workflow references it like this:

```yaml
${{ secrets.GITEATOKEN }}
```

Do not write the token anywhere in the repository.

## Registry image name

The workflow builds and pushes this image name:

```text
host.docker.internal:3000/<owner>/<repo>
```

For example, if your Gitea username is `murat` and repo name is `price-helper`, the image will be:

```text
host.docker.internal:3000/murat/price-helper
```

## How to verify branch behaviour

### Non-main branch

Create and push a branch:

```bash
git checkout -b feature/test-pipeline
git add .
git commit -m "add ci cd homework"
git push origin feature/test-pipeline
```

In Gitea Actions, verify:

- `lint` is green
- `test` is green
- `build-and-push` is green
- Docker build step is green
- Registry login and push steps are skipped

This proves non-`main` branches build but do not push.

### Main branch

Merge or push to `main`:

```bash
git checkout main
git merge feature/test-pipeline
git push origin main
```

In Gitea Actions, verify:

- `lint` is green
- `test` is green
- `build-and-push` is green
- Docker build step is green
- Registry login step is green
- Both push steps are green

## How to verify package tags

Open your repository in Gitea and go to:

```text
Packages
```

You should see the Docker image with both tags:

```text
latest
<short-sha>
```

## How to pull the pushed image

Find the short SHA from the successful `main` pipeline logs.

Then run:

```bash
docker pull host.docker.internal:3000/<owner>/<repo>:<short-sha>
```

Example:

```bash
docker pull host.docker.internal:3000/murat/price-helper:a1b2c3d
```

Run it:

```bash
docker run --rm host.docker.internal:3000/<owner>/<repo>:<short-sha>
```

Expected output:

```text
Original price: 250.0
Discount: 20.0%
Final price: 200.0
```

## Required screenshots for submission

Add these screenshots to your homework submission:

1. Successful pipeline run on a non-`main` branch. All three jobs must be green, but registry login and push steps must be skipped.
2. Successful pipeline run on `main`. All three jobs and push steps must be green.
3. Gitea Packages tab showing both `latest` and `<short-sha>` tags.
4. Terminal output showing successful `docker pull host.docker.internal:3000/<owner>/<repo>:<short-sha>`.

## Notes

- The token is used only through `${{ secrets.GITEATOKEN }}`.
- The Docker image is always built on every branch.
- The Docker image is pushed only when `github.ref == 'refs/heads/main'`.
- The short SHA is computed dynamically inside the workflow.
