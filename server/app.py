import os
from datetime import timedelta
from flask import Flask, request, json, jsonify, Response, redirect
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from passlib.hash import pbkdf2_sha256
from flask_cors import CORS
import stripe
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

from logger import logger, werk_logger
from mongodb_handler import MongoDBHandler
from utils import generate_key

# Get env variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Mail app
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.getenv('MAIL_PASSWORD')
}
app.config.update(mail_settings)
mail = Mail(app)

# Stripe configuration
STRIPE_KEYS = {
    'secret_key': os.getenv('STRIPE_SECRET_KEY'),
    'publishable_key': os.getenv('STRIPE_PUBLISHABLE_KEY'),
    'endpoint_secret': os.getenv('ENDPOINT_SECRET')
}

stripe.api_key = STRIPE_KEYS['secret_key']

# CORS configuration
# CORS(app, resources={r'/*': {'origins': 'http://127.0.0.1:3000'}})
CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = '890809-7907238094723'  # TODO. Put it in .env?
app.config['SECRET_KEY'] = 'll,lkmmomklmkm'  # TODO. Put it in .env?
app.config['SECURITY_PASSWORD_SALT'] = 'fsafasdsf'  # TODO. Put it in .env?
JWT = JWTManager(app)

# Instantiate DBHandler
db_handler = MongoDBHandler()  # Instance DB Handler



# ROUTES
@app.route('/')
def hello_world():
    return '<p>Hello universe from flask testing!</p>'


@app.route('/test-send-email', methods=['GET'])
def test_send_email():

    logger.debug('test_send_email...')

    try:
        msg = Message()
        msg.subject = "CCD test Subject"
        msg.recipients = [f"{app.config.get('MAIL_USERNAME')}@gmail.com"]
        msg.sender = app.config.get('MAIL_USERNAME')
        msg.body = 'CCD test body'
        response = mail.send(msg)
        status = 200
        logger.debug('test_send_email - Success')

    except Exception as err:
        response = err
        status = 400
        logger.error(f'test_send_email - {err}')

    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')

# STRIPE
@app.route('/config')
def get_publishable_key():

    logger.debug('get_publishable_key...')
    try:
        response = {
            'publicKey': STRIPE_KEYS['publishable_key']
        }
        status = 200
        logger.debug('get_publishable_key - Success')

    except Exception as err:
        response = err
        status = 400
        logger.error(f'test_send_email - {err}')

    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')
    # return jsonify({'publicKey': STRIPE_KEYS['publishable_key']})


@app.route('/stripe-line-items', methods=['GET'])
def get_stripe_line_items():

    try:
        plan = request.args.get('plan', default='undefined', type=str)
        line_items = [{"price": "", "quantity": 1}]

        if 'test' in STRIPE_KEYS['publishable_key']:  # Development
            if plan == 'Basic':
                line_items[0]['price'] = "price_1KuK6AKwbnjaoJWKI7BYGxLv"
            elif plan == 'Advanced':
                line_items[0]['price'] = "price_1L0IM3KwbnjaoJWK6nC4YunU"

        else:  # Production
            if plan == 'Basic':
                line_items[0]['price'] = "price_1KtXBtKwbnjaoJWK08eWnwQA"
            elif plan == 'Advanced':
                line_items[0]['price'] = "price_1LlAUIKwbnjaoJWK2Qu4vsqe"

    except Exception as err:
        response = err
        status = 400
        logger.error(f'get_stripe_line_items - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    return Response(response=json.dumps(line_items), status=200,
                    mimetype='application/json')


def stripe_create_customer(email: str, name: str):

    logger.debug('stripe_create_customer...')
    try:
        res = stripe.Customer.create(email=email, name=name)
        query_params = {'email': email}
        updated_data = {'stripeCustomerId': res['id']}
        response = db_handler.update(query_params=query_params, updated_data=updated_data)
        status = 200
        logger.debug('stripe_create_customer - Success')

    except Exception as err:
        response = err
        status = 400
        logger.error(f'stripe_create_customer - {err}')

    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')


@app.route('/create-subscription', methods=['POST'])
def stripe_create_subscription():

    logger.debug('stripe_create_subscription...')
    data = json.loads(request.data)
    try:
        price_id = data['priceId']
        query_params = {'email': data['email']}
        user = db_handler.read(query_params=query_params)
        customer_id = user['stripeCustomerId']

    except Exception as err:
        status = 400
        logger.error(f'stripe_create_subscription - {err}')
        return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

    try:
        # Create the subscription. Note we're expanding the Subscription's
        # latest invoice and that invoice's payment_intent
        # so we can pass it to the front end to confirm the payment
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )
        response = {
            'subscriptionId': subscription.id,
            'clientSecret': subscription.latest_invoice.payment_intent.client_secret
        }
        status = 200
        logger.debug('stripe_create_subscription - Success')
        # return jsonify(subscriptionId=subscription.id, clientSecret=subscription.latest_invoice.payment_intent.client_secret)

    except Exception as err:
        status = 400
        logger.error(f'stripe_create_subscription - {err}')
        return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

        # return jsonify(error={'message': err.user_message}), 400

    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')


def set_subscription_status(user_email: str, sub_status: bool):

    logger.debug('set_subscription_status...')
    query_params = {'email': user_email}
    try:
        user = db_handler.read(query_params=query_params)

    except Exception as err:
        status = 400
        logger.error(f'set_subscription_status - {err}')
        return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

    # Check if user exists
    if not user:
        response = 'User (email) does not exists!'
        status = 400
        logger.error(f'set_subscription_status - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    updated_data = {'subscriptionStatus': sub_status}
    response = db_handler.update(query_params=query_params, updated_data=updated_data)
    status = 200
    logger.debug('stripe_create_subscription - Success')

    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')


@app.route('/webhook', methods=['POST'])
def webhook():

    logger.debug('webhook...')

    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature', None)

    if not sig_header:
        response = 'No Signature Header'
        status = 400
        logger.error(f'webhook - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_KEYS['endpoint_secret']
        )
    except ValueError as err:
        # Invalid payload
        raise err
    except stripe.error.SignatureVerificationError as err:
        # Invalid signature
        raise err

    # Handle the event
    try:
        if event['type'] == 'invoice.payment_succeeded':
            user_email = event['data']['object']['customer_email']
            amount_paid = event['data']['object']['amount_paid']
            set_subscription_status(user_email=user_email, sub_status=True)
            select_plan(user_email=user_email, amount_paid=amount_paid)

        elif event['type'] == 'invoice.payment_failed':
            user_email = event['data']['object']['customer_email']
            set_subscription_status(user_email=user_email, sub_status=False)

        else:
            logger.debug('Unhandled event type {}'.format(event['type']))

    except Exception as err:
        response = 'No Signature Header'
        status = 400
        logger.error(f'webhook - {response}')
        return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

    status = 200
    logger.debug('webhook - Success')

    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')

    # return jsonify(success=True)


# USER MANAGEMENT
@app.route('/me', methods=['GET'])
def me():

    logger.debug('me...')
    jwt = request.headers.get('Authorization', None)

    if jwt:
        # Retrieve user details from the DB
        jwt = jwt.split(' ')[-1]
        query_params = {'jwt': jwt}
        user = db_handler.read(query_params=query_params)

        # Check if user exists
        if not user:
            response = 'User does not exists!'
            status = 400
            logger.error(f'me - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

        relevant_keys = {'username', 'email', 'plan', 'apiKey'}
        user = {key:value for key, value in user.items() if key in relevant_keys}
        reponse = user
        status = 200
        logger.debug(f'me - Success - {user}')
        return user

    response = 'No JWT provided'
    status = 400
    logger.error(f'me - {response}')
    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')


@app.route('/login', methods=['POST'])
def login():

    logger.debug('login...')

    try:
        body = request.get_json()
        email = body['email']
        password = body['password']

    except Exception as err:
        response = err
        status = 400
        logger.error(f'login - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    if email and password:
        # Retrieve user details from the DB
        # query_params = {a:data[a] for a in ['email'] if a in data}  # TEST this (try/except this line?)
        query_params = {'email': email}
        user = db_handler.read(query_params=query_params)

        # Check if user exists
        if not user:
            response = 'User (email) does not exists!'
            status = 400
            logger.error(f'login - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

        # Check if password is correct
        # if not pbkdf2_sha256.verify(data['password'], user['password']):


        if not pbkdf2_sha256.verify(password, user['password']):
            response = 'Incorrect password!'
            status = 400
            logger.error(f'login - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

        try:
            # jwt = create_access_token(identity=data['email'])
            jwt = create_access_token(identity=email)
            updated_data = {'jwt': jwt}
            output=db_handler.update(query_params=query_params, updated_data=updated_data)
            response = jwt
            status = 200
            logger.debug(f'login - Success - {user}')
            return response

        except Exception as err:
            status = 400
            logger.error(f'login - {err}')
            return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

    response = 'No email and/or password provided'
    status = 400
    logger.error(f'login - {response}')
    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')

    # print('No data', flush=True)
    # return ''


@app.route('/logout', methods=['GET'])
def logout():

    logger.debug('logout...')
    jwt = request.headers.get('Authorization', None)

    if jwt:
        # Retrieve user details from the DB
        jwt = jwt.split(' ')[-1]
        query_params = {'jwt': jwt}
        user = db_handler.read(query_params=query_params)

        # Check if user exists
        if not user:
            response = 'User does not exists!'
            status = 400
            logger.error(f'logout - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

        try:
            updated_data = {'jwt': ''}
            db_handler.update(query_params=query_params, updated_data=updated_data)
            status = 200
            logger.debug(f'logout - Success')
            return Response(status=status,
                        mimetype='application/json')

        except Exception as err:
            status = 400
            logger.error(f'logout - {err}')
            return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

    response = 'No JWT provided'
    status = 400
    logger.error(f'logout - {response}')
    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')


@app.route('/user', methods=['GET'])
def get_user():

    logger.debug('get_user...')

    try:
        body = request.get_json()
        jwt = body['jwt']

    except Exception as err:
        response = err
        status = 400
        logger.error(f'get_user - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')


    jwt = request.args.get('jwt', default=None, type=str)

    if jwt:
        # Retrieve user details from the DB
        query_params = {'jwt': jwt}
        user = db_handler.read(query_params=query_params)

        # Check if user exists
        if not user:
            response = 'User (email) does not exists!'
            status = 400
            logger.error(f'get_user - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')
        return user

    response = 'No JWT provided'
    status = 400
    logger.error(f'get_user - {response}')
    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')

    # print('No data', flush=True)
    # return ''


def generate_confirmation_token(email: str):

    logger.debug('generate_confirmation_token...')

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token: str, expiration: int = 3600):

    logger.debug('confirm_token...')

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except Exception as err:
        logger.error(f'confirm_token - Fail: {err}')
        return False

    logger.debug('confirm_token - Success - Token confirmed')
    return email


@app.route('/verify-JWT', methods=['POST'])
def verify_JWT():

    """ Verify user email with DB """

    logger.debug('verify_JWT...')

    # data = request.json
    jwt = request.args.get('jwt', default=None, type=str)

    if jwt:
        email = confirm_token(token=jwt)

        if not email:
            response = 'The confirmation link is invalid or it has expired.'
            status = 400
            logger.error(f'verify_JWT - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

    status = 200
    logger.debug('verify_JWT - Success')
    return Response(response=json.dumps(True), status=status,
                    mimetype='application/json')


@app.route('/signup', methods=['POST'])
def signup():

    logger.debug('signup...')

    try:
        body = request.get_json()
        username =body['username']
        email =body['email']
        password =body['password']

    except Exception as err:
        response = err
        status = 400
        logger.error(f'signup - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    # Encrypt password
    password = pbkdf2_sha256.encrypt(password)

    # Check if email exists
    # query_params = {a:data[a] for a in ['email'] if a in data}
    query_params = {'email': email}
    if len(db_handler.read(query_params=query_params)) > 0:
        response = 'Email already exists!'
        status = 400
        logger.error(f'signup - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    insert_data = {'username': username, 'email': email, 'password': password}
    response = db_handler.insert(insert_data)

    # TODO. Review
    # stripe_create_customer(email=data['email'], name=data['username'])  # Create user also in Stripe

    # Generate user emailVerificationJWT
    email_verif_jwt = generate_confirmation_token(email)
    updated_data = {'emailVerificationJWT': email_verif_jwt}
    db_handler.update(query_params=query_params, updated_data=updated_data)

    # TODO. Consider moving this to another function
    # Send email with reset password link including emailVerificationJWT
    msg = Message()
    msg.subject = "Email Verification for Crypto Candle Data"
    msg.recipients = [email]
    msg.sender = os.getenv('MAIL_USERNAME')
    url = os.path.join(os.getenv('BASE_URL'), 'emailVerification')
    msg.body = f"Please click the link to validate your email: {url}/?token={email_verif_jwt}"
    #mail.send(msg)

    status = 200
    logger.debug('signup - Success')
    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')

@app.route('/verify-email', methods=['POST'])
def verify_email():

    """ Verify user email against the DB """

    logger.debug('verify_email...')

    try:
        body = request.get_json()
        email_verif_jwt = body['emailVerificationJWT']

    except Exception as err:
        response = err
        status = 400
        logger.error(f'verify_email - {response}')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    if email_verif_jwt:
        # query_params = {a:data[a] for a in ['emailVerificationJWT'] if a in data}
        query_params = {'emailVerificationJWT': email_verif_jwt}
        user = db_handler.read(query_params=query_params)

        # Check if user exists
        if not user:
            response = 'User (email) does not exists!'
            status = 400
            logger.error(f'verify_email - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

        email = confirm_token(token=email_verif_jwt)

        if not email:
            response = 'The confirmation link is invalid or has expired.'
            status = 400
            logger.error(f'verify_email - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

    # Update password
    updated_data = {'emailVerified': True}
    response = db_handler.update(query_params=query_params, updated_data=updated_data)

    status = 200
    logger.debug('verify_email - Success')
    return Response(response=json.dumps(True), status=status,
                    mimetype='application/json')


@app.route('/reset-password', methods=['POST'])
def reset_password():

    logger.debug('reset_password...')

    # data = request.json
    # print('/reset-password data ' + str(data), flush=True)
    body = request.get_json()
    email = body['email']
    #email = request.args.get('email', default=None, type=str)
   
    if email:
        # query_params = {a:data[a] for a in ['email'] if a in data}
        query_params = {'email': email}
        user = db_handler.read(query_params=query_params)

        # Check if user exists
        if not user:
            response = 'User (email) does not exists!'
            status = 400
            logger.error(f'reset_password - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

    # Generate user resetPwdJWT
    reset_pwd_jwt = generate_confirmation_token(email)
    updated_data = {'resetPwdJWT': reset_pwd_jwt}
    db_handler.update(query_params=query_params, updated_data=updated_data)

    # Send email with reset password link including resetPwdJWT
    msg = Message()
    msg.subject = "Password Reset Request for Crypto Candle Data"

    msg.recipients = [email]
    msg.sender = os.getenv('MAIL_USERNAME')
    url = os.path.join(os.getenv('BASE_URL'), 'resetPwd')
    msg.body = f"This is the link to reset your password: {url}/?token={reset_pwd_jwt}"
    #res = mail.send(msg)

    status = 200
    logger.debug('reset_password - Success')
    return Response(response=json.dumps( 'success'), status=status,
                    mimetype='application/json')


@app.route('/update-password', methods=['POST'])
def update_password():

    logger.debug('update_password...')

    # data = request.json
    # print('/update-password data ' + str(data), flush=True)
    reset_pwd_jwt = request.args.get('resetPwdJWT', default=None, type=str)
    password = request.args.get('password', default=None, type=str)

    if reset_pwd_jwt:
        # query_params = {a:data[a] for a in ['resetPwdJWT'] if a in data}
        query_params = {'resetPwdJWT': reset_pwd_jwt}
        user = db_handler.read(query_params=query_params)

        # Check if user exists
        if not user:
            response = 'User (email) does not exists!'
            status = 400
            logger.error(f'update_password - {response}')
            return Response(response=json.dumps(response), status=status,
                            mimetype='application/json')

    # Encrypt password
    password = pbkdf2_sha256.encrypt(password)

    # Update password
    updated_data = {'password': password}
    response = db_handler.update(query_params=query_params, updated_data=updated_data)

    status = 200
    logger.debug('update_password - Success')
    return Response(response=json.dumps(True), status=status,
                    mimetype='application/json')


def select_plan(user_email: str, amount_paid: int):

    logger.debug('select_plan...')

    # Convert amount paid to EUR (from CENTS)
    amount_paid = amount_paid / 100

    query_params = {'docType': 'config'}
    doc = db_handler.read(query_params=query_params)

    try:
        pricing_dict = doc['pricePerPlan']

    except Exception as err:
        status = 400
        logger.error(f'select_plan - {err}')
        return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

    for key, value in pricing_dict.items():
        if float(value) == amount_paid:
            selected_plan = key

    query_params = {'email': user_email}
    updated_data = {'plan': selected_plan}
    response = db_handler.update(query_params=query_params, updated_data=updated_data)

    status = 200
    logger.debug('select_plan - Success')
    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')


@app.route('/generate-api-key', methods=['GET'])
def generate_apikey():

    logger.debug('generate_apikey...')

    email = request.args.get('email', default=None, type=str)

    if email:
        # Update or add APIKey to user in the DB
        query_params = {'email': email}
        updated_data = {'apiKey': generate_key()}
        response = db_handler.update(query_params=query_params, updated_data=updated_data)
        status = 200
        logger.debug('select_plan - Success')
        return Response(response=json.dumps(response), status=status,
                        mimetype='application/json')

    response = 'No email provided'
    status = 400
    logger.error(f'generate_apikey - {response}')
    return Response(response=json.dumps(response), status=status,
                    mimetype='application/json')


@app.route('/pricing', methods=['GET'])
def get_pricing():

    # Retrieve user details from the DB
    query_params = {'docType': 'config'}
    doc = db_handler.read(query_params=query_params)

    try:
        pricing = doc['pricePerPlan']

    except Exception as err:
        status = 400
        logger.error(f'get_pricing - {err}')
        return Response(response=json.dumps(err), status=status,
                        mimetype='application/json')

    return pricing
