import urllib.request
import urllib.error
from urllib.parse import urlparse

def get_robots_txt(base_url: str, user_agent:str="FlexScraper/1.0"):
    """
    Get robots.txt of the site
    """
    
    headers = {
        "User-Agent": user_agent
    }
    robots_url = base_url.rstrip("/") + "/robots.txt"
    request = urllib.request.Request(robots_url, headers=headers)
    
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def is_authorized_to_parse(page_url: str, user_agent: str = "FlexScraper/1.0") -> bool:
    """Check if the user agent is authorized to parse the page"""

    try:
        parsed = urlparse(page_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        robots_txt = get_robots_txt(base_url, user_agent)
    except Exception:
        # robots.txt inaccessible → autorisé par défaut
        return True

    path = parsed.path or "/"

    rules = {}
    current_agent = None

    # Parsing du robots.txt
    for line in robots_txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.lower().startswith("user-agent"):
            current_agent = line.split(":", 1)[1].strip()
            rules[current_agent] = {"allow": [], "disallow": []}

        elif current_agent:
            directive, value = line.split(":", 1)
            directive = directive.lower().strip()
            value = value.strip()

            if directive == "allow":
                rules[current_agent]["allow"].append(value)
            elif directive == "disallow":
                rules[current_agent]["disallow"].append(value)

    # Règles spécifiques au User-Agent
    if user_agent in rules:
        agent_rules = rules[user_agent]
    # Sinon nous sommes un User-Agent * si spécifié
    elif "*" in rules:
        agent_rules = rules["*"]
    # Aucune règle → autorisé
    else:
        return True

    # Application des règles
    allowed = True

    for allowed_path in agent_rules["allow"]:
        if allowed_path == "*" or path.startswith(allowed_path):
            allowed = True

    for disallowed in agent_rules["disallow"]:
        if disallowed and path.startswith(disallowed):
            allowed = False
            
    return allowed
