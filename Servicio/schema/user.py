from pydantic import BaseModel, Field




class User(BaseModel):
    user_id : int | None =  None
    username: str = Field(..., description='employee_id is user',json_schema_extra={"example": "6205036053"} )
    password: str = Field(..., description= 'initially is identificaction of employee', json_schema_extra={"example": "2068345351"})
    role_id: int = Field(..., description='according to the job position',json_schema_extra={"example": 2002} )


class ChangePassword(BaseModel):
    username: str =Field(..., description='username',json_schema_extra={"example": "6205036053"} )
    previous_password: str = Field(..., description='old password',json_schema_extra={"example": "12345678"} )
    new_password: str = Field(..., description='new password',json_schema_extra={"example": "87654321"} )
    repeat_password:str =  Field(..., description='repaet password',json_schema_extra={"example": "87654321"} )