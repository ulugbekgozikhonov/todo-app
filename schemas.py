from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
	title: str = Field(min_length=3)
	description: str = Field(min_length=5)
	owner_id: int
	priority: int = Field(gt=0, lt=6)
	completed: bool = Field(default=False)


class RegisterSchema(BaseModel):
	first_name: str = Field(min_length=5)
	last_name: str = Field(min_length=5)
	email: str = Field(min_length=5)
	password: str = Field(min_length=4)
	age: int = Field(gt=18, lt=100)
	username: str = Field(min_length=3)


class LoginSchema(BaseModel):
	username: str = Field(min_length=3)
	password: str = Field(min_length=4)
