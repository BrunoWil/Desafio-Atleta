# run:
# 	@uvicorn main:app --reload

# create-migration:
# 	@PYTHONPATH=$(shell pwd) alembic revision --autogenerate -m $(d)

# run-migrations:
# 	@PYTHONPATH=$(shell pwd) alembic upgrade head


run:
	@uvicorn main:app --reload

create-migration:
	@set PYTHONPATH=. && alembic revision --autogenerate -m $(d)

cm:
	@set PYTHONPATH=. && alembic revision --autogenerate -m $(d)

run-migrations:
	@set PYTHONPATH=. && alembic upgrade head

rm:
	@set PYTHONPATH=. && alembic upgrade head