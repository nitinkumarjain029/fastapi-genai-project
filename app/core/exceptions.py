from fastapi import Request
from fastapi.responses import JSONResponse



class UserNotFoundException(Exception):
    pass

class EmailAlreadyExistsException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

async def user_not_found_exception_handler(request: Request, exc : UserNotFoundException):
    return JSONResponse(
        status_code = 404,
        content = {
            "detail": "User Not Found"
        }
    )

async def email_already_exists_exception_handler(request : Request, exc : EmailAlreadyExistsException):
    return JSONResponse(
        status_code = 409,
        content = {
            "detail": "Email already Exists"
        }
    )

async def global_exception_handler(request: Request, exc : Exception):
    return JSONResponse(
        status_code = 500,
        content = {
            "detail" : "internal server error"
        }
    )
