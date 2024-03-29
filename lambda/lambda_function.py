from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.create_url import create_url
from src.get_url import get_url

cors_config = CORSConfig(
    allow_origin="*", max_age=300
)
app = APIGatewayRestResolver(cors=cors_config)


@app.post("/create")
def creates_url():
    long_url = app.current_event.json_body["long_url"]
    return create_url(long_url)


@app.get("/<short_id>", cors=True)
def gets_url(short_id):
    return get_url(short_id)


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    if 'httpMethod' not in event:
        return {"statusCode": 400, "body": "Invalid request"}
    return app.resolve(event, context)
