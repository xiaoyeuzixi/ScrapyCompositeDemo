import aiohttp
import logging

class AuthorizationMiddleware(object):
    # 指定账号池的URL，用于获取授权凭证
    accountpool_url = 'http://192.168.110.112:6778/antispider7/random'
    # 设置日志记录器，用于记录中间件的日志信息
    logger = logging.getLogger('middlewares.authorization')

    async def process_request(self, request, spider):
        """
        在请求处理过程中，为请求设置Authorization头部。
        
        参数:
        - request: Scrapy的请求对象，代表待处理的HTTP请求
        - spider: 当前爬虫对象，代表正在运行的爬虫实例
        """
        # 使用aiohttp创建一个异步HTTP会话
        async with aiohttp.ClientSession() as client:
            # 发送GET请求到账号池服务，获取授权凭证
            response = await client.get(self.accountpool_url)
            # 如果返回的状态码不是200，说明请求失败，直接返回
            if not response.status == 200:
                return
            # 从响应中提取文本内容，即授权凭证
            credential = await response.text()
            # 将授权凭证添加到请求头部的Authorization字段中
            authorization = f'jwt {credential}'
            self.logger.debug(f'set authorization {authorization}')
            request.headers['authorization'] = authorization

class ProxyMiddleware(object):
    # 指定代理池的URL，用于获取代理地址
    proxypool_url = 'http://192.168.110.112:5555/random'
    # 设置日志记录器，用于记录中间件的日志信息
    logger = logging.getLogger('middlewares.proxy')

    async def process_request(self, request, spider):
        """
        在请求处理过程中，为请求设置代理。
        
        参数:
        - request: Scrapy的请求对象，代表待处理的HTTP请求
        - spider: 当前爬虫对象，代表正在运行的爬虫实例
        """
        # 使用aiohttp创建一个异步HTTP会话
        async with aiohttp.ClientSession() as client:
            # 发送GET请求到代理池服务，获取代理地址
            response = await client.get(self.proxypool_url)
            # 如果返回的状态码不是200，说明请求失败，直接返回
            if not response.status == 200:
                return
            # 从响应中提取文本内容，即代理地址
            proxy = await response.text()
            # 将代理地址添加到请求的meta字段中，以便通过该代理发送请求
            self.logger.debug(f'set proxy {proxy}')
            request.meta['proxy'] = f'http://{proxy}'
