# lambda/index.py
import json
import os
import re
import urllib.request

from botocore.exceptions import ClientError

# 環境変数から FastAPI エンドポイントを取得
API_BASE = "https://0e89-34-16-242-246.ngrok-free.app"
GENERATE_PATH = "/generate"


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # リクエストボディ解析
        body = json.loads(event.get('body', '{}'))
        prompt = body.get('message', '')

        # API_ENDPOINT の確認
        if not API_BASE:
            raise Exception("API_ENDPOINT is not set")
        url = API_BASE.rstrip('/') + GENERATE_PATH

        # FastAPI /generate へ POST リクエスト用ペイロードを準備
        request_payload = {
            "prompt": prompt
        }
        data = json.dumps(request_payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        # リクエスト送信とレスポンス取得
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        # FastAPI の応答を取得
        assistant_response = result.get('generated_text', '')

        # API Gateway へ返却する形式
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"success": False, "error": str(error)})
        }
# lambda/index.py
import json
import os
import re
import urllib.request

from botocore.exceptions import ClientError

# 環境変数から FastAPI エンドポイントを取得
API_BASE = os.environ.get("API_ENDPOINT")
GENERATE_PATH = "/generate"

# Lambda コンテキストからリージョンを抽出（未使用）
def extract_region_from_arn(arn):
    match = re.search(r'arn:aws:lambda:([^:]+):', arn)
    return match.group(1) if match else "us-east-1"


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # リクエストボディ解析
        body = json.loads(event.get('body', '{}'))
        prompt = body.get('message', '')

        # API_ENDPOINT の確認
        if not API_BASE:
            raise Exception("API_ENDPOINT is not set")
        url = API_BASE.rstrip('/') + GENERATE_PATH

        # FastAPI /generate へ POST リクエスト用ペイロードを準備
        request_payload = {
            "prompt": prompt
        }
        data = json.dumps(request_payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        # リクエスト送信とレスポンス取得
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        # FastAPI の応答を取得
        assistant_response = result.get('generated_text', '')

        # API Gateway へ返却する形式
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"success": False, "error": str(error)})
        }
