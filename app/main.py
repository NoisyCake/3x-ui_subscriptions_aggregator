import os
import httpx
import base64
import logging
from asyncio import gather
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Response, HTTPException


# Настройки логирования
logging.basicConfig(
    level=logging.WARNING, filename='script_log.log',
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

load_dotenv()
path = os.getenv('URL')


# Функция для получения подписок по URL и последующего декодирования данных в base64
async def fetch_subscription(client, sub_url: str, sub_id: str) -> Optional[bytes]:
    try:
        sub = await client.get(f'{sub_url}{sub_id}', timeout=10)
        sub.raise_for_status()
        return base64.b64decode(sub.text)
    except httpx.HTTPError as e:
            logger.error(f"Can't get subscription url from {sub_url}{sub_id}: {str(e)}")
    except ValueError as e:
            logger.error(f"Can't decode base64 for {sub_url}{sub_id}: {str(e)}")
        
        
# Функция для объединения подписок
@app.get(f'/{path}/{{sub_id}}')
async def merge_subscriptions(sub_id: str) -> Response:
    sub_urls = os.getenv('SUB_URLS').split()
    
    if not sub_urls:
        logger.error("Servers not found")
        raise HTTPException(status_code=500, detail="Servers not found")
    
    
    async with httpx.AsyncClient() as client:
        decoded_subs = [fetch_subscription(client, sub_url, sub_id) for sub_url in sub_urls]
        results = await gather(*decoded_subs)
        data = [result for result in results if result is not None]
        
        if not data:
            logger.error("No subscriptions available")
            raise HTTPException(status_code=500, detail="No subscriptions available")    
        
        # Объединение декодированных подписок с последующей кодировкой в base64
        merged_subs = b''.join(data)
        global_sub = base64.b64encode(merged_subs)
        
        # Возврат результата в виде обычного текста
        return Response(content=global_sub, media_type='text/plain')
