# Dev log

## Kickoff: Oct 30 – Nov 7, 2026

**Time spent:** 2 hrs

### What got done

- Dev environment on a System76 laptop (Pop!_OS): Eclipse Temurin JDK 17, IntelliJ IDEA, Git with a GitHub SSH key, and Docker Engine with the compose plugin.
- Created the `realtime-fraud-platform` repo as a Gradle multi-project build (Groovy DSL). The Gradle wrapper and `settings.gradle` live at the root.
- Generated `payment-api` from start.spring.io: Spring Boot 4.1.x, Java 17, YAML config, with Web, Validation, and Actuator.
- CI with GitHub Actions: `./gradlew build` runs on every PR and every push to `main`. `main` is protected by a required build check, and work lands through squash-merged PRs.
- PostgreSQL 17 running locally from `infra/docker-compose.yml`.
- Python virtual environment in `ml/`, plus `ml/explore.py` to profile the PaySim dataset. The CSV lives in `data/` and is git-ignored.

### PaySim findings

<!-- Check these against your own explore.py output -->
- **Rows:** 6,362,620
- **Fraud:** 8,213 transactions, about **0.13%**
- **Fraud appears only in `TRANSFER` and `CASH_OUT`.** `PAYMENT`, `CASH_IN`, and `DEBIT` contain none.
- **What this means:**
  - Accuracy is useless as a metric. A model that always says "not fraud" scores about 99.87% while catching nothing, so Week 7 will use precision, recall, and PR-AUC.
  - Scoring can concentrate on two transaction types.

### Decisions and why

- **Java 17 only.** It's still a common production baseline at banks. Skip Java 21 features such as virtual threads and pattern matching in switch.
- **Gradle multi-project instead of Maven.** One `./gradlew build` covers every service, and a shared `common-events` module (Week 5) keeps the Kafka event classes in one place.
- **Groovy DSL** for the build files rather than Kotlin.
- **YAML** for Spring config, since the Kafka, datasource, and Actuator settings are deeply nested.
- **PRs and squash merges even as a solo developer.** This gives a clean `main` history and shows a team workflow.

### Problems and fixes

- **`mv: cannot stat 'payment-api/gradlew.bat'`**
  - *Cause:* an earlier run had already moved the wrapper. With several files, `mv` moves the ones it finds and reports the rest.
  - *Lesson:* check the current state with `ls -a` or `find` before re-running a command.
- **Leftover `payment-api/settings.gradle`**
  - *Cause:* a `settings.gradle` inside a subfolder makes Gradle treat that folder as its own separate build.
  - *Fix:* keep only the root `settings.gradle`.
- **GitHub's Java `.gitignore` template ignores `*.jar`**
  - *Cause:* that pattern also ignored `gradle/wrapper/gradle-wrapper.jar`. The build would pass locally but fail in CI, because a fresh checkout wouldn't have the jar.
  - *Fix:* add the exception `!gradle/wrapper/gradle-wrapper.jar`, plus the Gradle, IntelliJ, sbt, and Python ignore lines.
  - *Check:* `git check-ignore -v` shows the matching rule. If that rule starts with `!`, the file is **not** ignored.
- **`git branch -d` warned "not yet merged to HEAD"**
  - *Cause:* a squash merge creates a brand-new commit on `main`, so Git can't see that the branch was merged. The warning is harmless.
  - *Fix:* turned on "Automatically delete head branches" in the repo settings.
- **`explore.py` failed outside the virtual environment**
  - *Cause:* pandas is installed only in `ml/.venv`.
  - *Fix:* run `source ml/.venv/bin/activate` first, or call the environment's Python directly with `ml/.venv/bin/python ml/explore.py`.

### Interview story candidates

- **Works locally, fails in CI.** A `.gitignore` rule silently excluded the Gradle wrapper jar. Spotted before CI broke and fixed with a negation rule. The theme is environment parity.
- **Reading the data before modeling.** A 0.13% fraud rate rules out accuracy as a metric, which shaped how the model will be evaluated.


