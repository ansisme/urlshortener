from .modules.dynamodb import get_dynamodb_table
from aws_lambda_powertools.event_handler import Response, content_types

table = get_dynamodb_table()


def get_url(short_id):
    try:
        item = table.get_item(Key={"short_id": short_id})
        long_url = item.get("Item").get("url")
        print("DynamoDB Response:", item)
    except:
        return {
            "statusCode": 301,
            "headers": {
                "Location": "https://objects.ruanbekker.com/assets/images/404-blue.jpg",
                "Access-Control-Allow-Origin": "*",  # Add CORS header
            },
        }

    return Response(
        status_code=301,
        content_type=content_types.APPLICATION_JSON,
        headers={
            "Location": long_url,
            "Access-Control-Allow-Origin": "*",  # Add CORS header
        },
    )
