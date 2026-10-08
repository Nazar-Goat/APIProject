from beanie import PydanticObjectId

from src.modules.articles.models import Article


class ArticleRepository:
    async def create(
            self,
            title:str,
            content:str,
            tags: list[str],
            author
    ) -> Article:
        article = Article(
            title = title,
            content = content,
            tags = tags,
            author = author
        )
        await article.insert()
        return article

    async def get_by_id(self, article_id: PydanticObjectId) -> Article | None:
        return await Article.find_one({"_id": article_id}, fetch_links=True)

    async def search(self, search_query: str | None, tag: str | None) -> list[Article]:
        filters = {}

        if search_query is not None:
            filters["$text"] = {"$search": search_query}

        if tag is not None:
            filters["tags"] = tag

        return await Article.find(filters).to_list()

    async def update(
            self,
            article: Article,
            update_data: dict,
    ) -> Article:

        await article.set(update_data)

        return article

    async def delete(self, article: Article) -> None:
        await article.delete()
