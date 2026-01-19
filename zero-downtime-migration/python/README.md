## Read the README of the Typescript File for a better understanding of the project, this is the python version of that

# step 0 - install dependencies

- pip install -r requirements.txt

# Step 1 — Add new columns

- python3 -m migrations.add_first_last_name

# Step 2 — Deploy dual-write API

- uvicorn app:app --reload

# Step 3 — Backfill existing data

- python3 -m scripts.backfill_names

# Step 4 — Remove old column

- python3 -m migrations.drop_full_name
