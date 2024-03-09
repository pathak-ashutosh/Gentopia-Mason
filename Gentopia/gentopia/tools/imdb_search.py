from imdb import IMDb
from gentopia.tools import BaseTool, Optional, Type, AnyStr, Any
from pydantic import BaseModel, Field

class ImdbSearchArgs(BaseModel):
    query: str = Field(..., description="a search query")
    
class ImdbSearch(BaseTool):
    """Tool that adds the capability to query the IMDb search API."""
    
    name = "imdb_search"
    description = ("A search engine retrieving top search results as snippets from IMDb."
                   "Input should be a search query.")
    
    args_schema: Optional[Type[BaseModel]] = ImdbSearchArgs
    
    def _run(self, query: AnyStr) -> str:
        ia = IMDb()
        movies = ia.search_movie(query)
        return '\n\n'.join([str(movie) for movie in movies])
    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
if __name__ == "__main__":
    ans = ImdbSearch()._run("The Matrix")
    print(ans)