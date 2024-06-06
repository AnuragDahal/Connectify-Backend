from fastapi import HTTPException, APIRouter, Request
from starlette.responses import RedirectResponse
from ..handlers.Auth.oauthHandler import google, generate_state, validate_token
from ..handlers.User.userhandler import Validate
from ..core.database import user_collection
from ..models.schemas import OauthUser

router = APIRouter(tags=['Google OAuth'], prefix='/api/v1/google')


@router.get('/login')
async def login(request: Request):
    state = generate_state()
    request.session['state'] = state
    print("state:", state)
    # here the auth refers to the route defined below not the auth module
    redirect_uri = request.url_for('auth')
    print(redirect_uri)
    return await google.authorize_redirect(request, redirect_uri, state=state)


@router.get('/auth')
async def auth(request: Request):
    # print(f"Callback URL: {request.url}")
    state = request.session.get('state')
    stateInQuery = request.query_params.get('state')
    if not state or state != request.query_params.get('state'):
        raise HTTPException(
            status_code=400, detail='Invalid state parameter.')

    token = await google.authorize_access_token(request)
    id_token = token.get('id_token')

    if not id_token:
        raise HTTPException(
            status_code=400, detail='Unable to authenticate.')

    try:
        claims = validate_token(id_token)
        # get the user details from the claims and add as user to the database

        username = claims.get('name')
        user_email = claims.get('email')
        isEmailVerified = claims.get('email_verified')
        profile_picture = claims.get('picture')

        # Check the user exists in the db or not
        isUser = Validate.verify_email(user_email)
        if not isUser:
            user_collection.insert_one({
                "name": username,
                "email": user_email,
                "profile_picture": profile_picture,
                "isEmailVerified": isEmailVerified,
            })
    except Exception as e:
        print(f"Token validation error: {e}")
        raise HTTPException(status_code=400, detail='Invalid token.')

    return RedirectResponse(url='/home')
