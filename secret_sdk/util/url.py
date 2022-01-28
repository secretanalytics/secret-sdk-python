from furl import furl  # type: ignore


def urljoin(base: str, url: str) -> str:
    if "?" in url and len(url.split("?")) > 1:
        url, query_params = url.split("?")
        return furl(base.rstrip("/")).add(path=url, query_params=query_params).url
    else:
        return furl(base.rstrip("/")).add(path=url).url
