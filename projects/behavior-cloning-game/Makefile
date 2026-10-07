PYTHON ?= python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
RUN_DIR := .local-run

.PHONY: deploy teardown run stop test venv

venv:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install -e '.[dev]' -r web/api/requirements.txt

deploy:
	npm --prefix infra/cdk run deploy

teardown:
	@npm --prefix infra/cdk run teardown && { \
	  printf '\nThe CDK stack was removed. These retained resources remain:\n'; \
	  printf '  - Private S3 artifacts bucket (datasets and trained models): empty it, then delete it in AWS Console > S3.\n'; \
	  printf '  - Cognito user pool (invited users): delete it in AWS Console > Amazon Cognito > User pools.\n'; \
	  printf 'Use the BehaviorLabPilot CloudFormation stack outputs to identify their names/IDs before teardown.\n'; \
	  printf 'The custom ACM certificate and DNS records are also external to the stack and remain.\n\n'; \
	}

run: venv
	npm --prefix web ci
	mkdir -p $(RUN_DIR)
	nohup $(VENV)/bin/uvicorn web.api.app:app --host 127.0.0.1 --port 8000 > $(RUN_DIR)/api.log 2>&1 & echo $$! > $(RUN_DIR)/api.pid
	cd web && nohup npm run dev -- --port 5173 > ../$(RUN_DIR)/web.log 2>&1 & echo $$! > $(RUN_DIR)/web.pid
	@echo 'Behavior Cloning Game running at http://127.0.0.1:5173'

stop:
	@for service in api web; do \
	  pid_file="$(RUN_DIR)/$$service.pid"; \
	  if [ -f "$$pid_file" ]; then \
	    pid=$$(cat "$$pid_file"); \
	    if kill -0 "$$pid" 2>/dev/null; then kill "$$pid"; fi; \
	    rm -f "$$pid_file"; \
	  fi; \
	done
	@echo 'Stopped local Behavior Cloning Game processes.'

	test:
	$(VENV_PYTHON) -m pytest
	npm --prefix web run build
