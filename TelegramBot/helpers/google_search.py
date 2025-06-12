from googlesearch import search
import asyncio
from typing import List, Dict
import aiohttp
from bs4 import BeautifulSoup
import re

async def fetch_page_content(url: str) -> Dict[str, str]:
    """
    Получает содержимое страницы и извлекает полезную информацию
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Извлекаем мета-теги
                    title = soup.title.string if soup.title else ""
                    description = ""
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if meta_desc:
                        description = meta_desc.get('content', '')
                    
                    # Ищем email адреса
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', html)
                    
                    # Ищем телефоны
                    phones = re.findall(r'\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}', html)
                    
                    return {
                        'url': url,
                        'title': title,
                        'description': description,
                        'emails': list(set(emails)),
                        'phones': list(set(phones))
                    }
    except Exception as e:
        return {
            'url': url,
            'error': str(e)
        }

async def google_search(query: str, num_results: int = 3) -> List[Dict[str, str]]:
    """
    Выполняет поиск в Google и анализирует результаты
    """
    def _search():
        results = []
        for url in search(query, num_results=num_results, stop=num_results):
            results.append(url)
        return results
    
    # Запускаем поиск в отдельном потоке
    loop = asyncio.get_event_loop()
    urls = await loop.run_in_executor(None, _search)
    
    # Анализируем каждую страницу
    tasks = [fetch_page_content(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    return results 